# Web Forms & Backend Communication

## Lesson Overview
This lesson covered how web forms communicate with a backend using HTTP methods like `POST` and `GET`. By the end of the session, students were expected to understand how to build forms that send data to a server efficiently and securely.

---

## What Was Covered
- How forms send data to a backend
- The difference between `GET` and `POST`
- Why passwords and sensitive data should not be sent using `GET`
- Structuring a modern login/signup form

---

## Form Basics
Forms are the standard way for users to submit information to a server. A basic example covered in the lesson:

```html
<form action="/login" method="POST">
   <label for="username">Username:</label>
   <input type="text" id="username" name="username" required />

   <label for="password">Password:</label>
   <input type="password" id="password" name="password" required />

   <button type="submit">Login</button>
</form>
```

Key takeaways:
- `action="/login"` specifies where the data will be sent.
- `method="POST"` ensures the data is sent securely within the request body.

---

## GET vs. POST
| Method | When to Use | Data Visibility | Example |
|--------|------------|----------------|---------|
| **GET** | Fetching data | Shown in URL (Not safe for passwords) | Searching on Google |
| **POST** | Sending data securely | Hidden in the request body | Logging in or signing up |

Important note: **Never use GET for sensitive data** as it exposes information in the URL, making it vulnerable to security risks.

---

## Summary
By the end of this lesson, students gained a solid understanding of how web forms interact with a backend, when to use `GET` vs. `POST`, and best practices for handling user input securely.

