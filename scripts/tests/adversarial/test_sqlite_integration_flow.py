import sqlite3
import tempfile
import unittest
from pathlib import Path


def init_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        create table if not exists runs (
            id integer primary key autoincrement,
            repo text not null,
            pr text not null,
            commit_sha text not null,
            status text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists findings (
            id integer primary key autoincrement,
            run_id integer not null,
            fingerprint text not null,
            severity text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists verdicts (
            id integer primary key autoincrement,
            run_id integer not null,
            fingerprint text not null,
            bucket text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists cleanup_events (
            id integer primary key autoincrement,
            run_id integer not null,
            action text not null
        )
        """
    )
    conn.commit()


def create_or_resume_run(conn: sqlite3.Connection, *, repo: str, pr: str, commit_sha: str) -> int:
    row = conn.execute(
        "select id from runs where repo = ? and pr = ? and commit_sha = ? order by id desc limit 1",
        (repo, pr, commit_sha),
    ).fetchone()
    if row:
        return int(row[0])
    cur = conn.execute(
        "insert into runs(repo, pr, commit_sha, status) values(?, ?, ?, ?)",
        (repo, pr, commit_sha, "open"),
    )
    conn.commit()
    return int(cur.lastrowid)


def write_verdict(conn: sqlite3.Connection, *, run_id: int, fingerprint: str, bucket: str) -> None:
    conn.execute(
        "insert into verdicts(run_id, fingerprint, bucket) values(?, ?, ?)",
        (run_id, fingerprint, bucket),
    )
    conn.commit()


def merge_cleanup(conn: sqlite3.Connection, *, run_id: int, retention_days: int) -> None:
    if retention_days <= 0:
        retention_days = 1
    conn.execute("insert into cleanup_events(run_id, action) values(?, ?)", (run_id, "archive-summary"))
    conn.execute("insert into cleanup_events(run_id, action) values(?, ?)", (run_id, "purge-artifacts"))
    conn.execute("insert into cleanup_events(run_id, action) values(?, ?)", (run_id, f"prune-{retention_days}d"))
    conn.execute("insert into cleanup_events(run_id, action) values(?, ?)", (run_id, "vacuum"))
    conn.execute("update runs set status = ? where id = ?", ("merged-cleaned", run_id))
    conn.commit()


class TestAdversarialSQLiteIntegrationFlow(unittest.TestCase):
    def test_run_resume_and_cleanup_flow_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "adversarial.db"
            conn = sqlite3.connect(db_path)
            init_schema(conn)

            run_id = create_or_resume_run(conn, repo="r", pr="12", commit_sha="abc")
            resumed = create_or_resume_run(conn, repo="r", pr="12", commit_sha="abc")
            write_verdict(conn, run_id=run_id, fingerprint="fp-1", bucket="high-confidence")
            write_verdict(conn, run_id=run_id, fingerprint="fp-2", bucket="contested")
            merge_cleanup(conn, run_id=run_id, retention_days=14)

            bucket_rows = conn.execute(
                "select fingerprint, bucket from verdicts where run_id = ? order by fingerprint",
                (run_id,),
            ).fetchall()
            status = conn.execute("select status from runs where id = ?", (run_id,)).fetchone()[0]
            cleanup_actions = conn.execute(
                "select action from cleanup_events where run_id = ? order by id",
                (run_id,),
            ).fetchall()
            conn.close()

        self.assertEqual(run_id, resumed)
        self.assertEqual(bucket_rows, [("fp-1", "high-confidence"), ("fp-2", "contested")])
        self.assertEqual(status, "merged-cleaned")
        self.assertEqual(
            [row[0] for row in cleanup_actions],
            ["archive-summary", "purge-artifacts", "prune-14d", "vacuum"],
        )


if __name__ == "__main__":
    unittest.main()
