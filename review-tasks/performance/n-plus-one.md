# Task: N+1 Query

## Category
performance

## Severity
high

## Platforms
web, api

## Languages
all

## Description
Loading a collection then executing a separate database query for each item in the collection, resulting in N+1 total queries instead of 1-2. Causes severe performance degradation at scale.

## Detection Heuristics
- Loop body contains database query or ORM lazy-load access
- Accessing related model attributes inside iteration without eager loading
- GraphQL resolvers that query per-item without DataLoader
- Nested serializer accessing relations without `select_related`/`prefetch_related`

## Eval Cases

### Case 1: Django lazy loading in loop
```python
def get_order_summary(request):
    orders = Order.objects.all()
    summaries = []
    for order in orders:
        summaries.append({
            'id': order.id,
            'customer': order.customer.name,  # lazy load per iteration
            'total': order.total
        })
    return JsonResponse(summaries, safe=False)
```
**Expected finding:** High — N+1 query. `order.customer.name` triggers a query per order. Use `Order.objects.select_related('customer').all()`

### Case 2: TypeORM without relations
```typescript
const posts = await postRepository.find();
for (const post of posts) {
  const author = await userRepository.findOne(post.authorId); // N queries
  post.authorName = author.name;
}
```
**Expected finding:** High — N+1 query. Load relations eagerly: `postRepository.find({ relations: ['author'] })`

## Counter-Examples

### Counter 1: Eager loading
```python
orders = Order.objects.select_related('customer').all()
for order in orders:
    print(order.customer.name)  # no additional query
```
**Why it's correct:** `select_related` joins the customer table in the initial query.

## Binary Eval Assertions
- [ ] Detects N+1 in eval case 1
- [ ] Detects N+1 in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests eager loading fix
- [ ] Severity assigned as high
