---
name: lang ruby
description: >
  Ruby-specific code review: Rails security (mass assignment, CSRF), ActiveRecord N+1, Ruby patterns.
  Trigger when reviewing Ruby (.rb) files, especially Rails applications, ActiveRecord models, or
  controllers with user input handling.
---

# Language-Specific Review: Ruby

## Purpose
Ruby and Rails-specific guidance: security, ActiveRecord pitfalls, and Ruby idioms.

## Key Areas

### 1. Rails Security
```ruby
# ❌ UNSAFE: Mass assignment
def create
  @user = User.new(params[:user])  # Allows role injection
end

# ✅ SAFE: Strong parameters
def create
  @user = User.new(user_params)
end

private
def user_params
  params.require(:user).permit(:name, :email)
end

# ❌ UNSAFE: CSRF protection disabled
class ApplicationController < ActionController::Base
  skip_before_action :verify_authenticity_token
end

# ✅ SAFE: Keep CSRF protection (default)
```

### 2. ActiveRecord N+1
```ruby
# ❌ BAD: N+1 queries
@users = User.all
@users.each do |user|
  puts user.profile.bio  # N+1
end

# ✅ GOOD: includes
@users = User.includes(:profile)
@users.each do |user|
  puts user.profile.bio
end
```

### 3. SQL Injection
```ruby
# ❌ UNSAFE: String interpolation
User.where("email = '#{params[:email]}'")

# ✅ SAFE: Parameterized
User.where("email = ?", params[:email])

# ✅ BETTER: Hash conditions
User.where(email: params[:email])
```

### 4. XSS in ERB
```erb
<!-- ❌ UNSAFE: raw HTML -->
<%= raw @user.bio %>

<!-- ✅ SAFE: Auto-escaped -->
<%= @user.bio %>

<!-- ✅ SAFE: Sanitize -->
<%= sanitize @user.bio %>
```

### 5. Command Injection
```ruby
# ❌ UNSAFE: Backticks
`ping #{params[:host]}`

# ✅ SAFE: Array form
system('ping', '-c', '4', params[:host])
```

## OWASP References
- [Ruby on Rails Security](https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html)

## Quick Checklist
- [ ] Strong parameters for mass assignment
- [ ] No SQL string interpolation
- [ ] includes/joins for N+1 prevention
- [ ] ERB auto-escaping (no raw)
- [ ] Command execution uses array form
