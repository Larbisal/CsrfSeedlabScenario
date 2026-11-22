<?php
/**
 * SEED Lab Task 4 — CSRF Token Defense
 *
 * This page is shown when Elgg blocks a request because the CSRF token is
 * invalid or missing.  It is reached only when:
 *   1. The student has removed the bypass line from Csrf.php  (defense active)
 *   2. An attack page submits a cross-site request without a valid token
 *
 * The flag is proof that the defense is working.
 * It is unique per sandbox (injected by Ansible into the container environment).
 */

$flag = getenv('FLAG_T4') ?: 'FLAG_T4_NOT_SET';
?>
<!DOCTYPE html>
<html>
<head>
  <title>CSRF Blocked — Task 4</title>
  <style>
    body { background:#1a2433; color:#fff; font-family:Arial,sans-serif;
           display:flex; flex-direction:column; align-items:center;
           justify-content:center; height:100vh; margin:0; }
    .card { background:#fff; color:#1a2433; border-radius:10px;
            padding:40px; max-width:560px; text-align:center; }
    h1    { color:#c4501a; }
    .flag { background:#1a2433; color:#4ade80; font-family:monospace;
            font-size:1.3em; padding:16px 24px; border-radius:6px;
            margin-top:20px; word-break:break-all; }
    p     { color:#4a5565; }
  </style>
</head>
<body>
  <div class="card">
    <h1>&#x1F6AB; Request Blocked!</h1>
    <p>
      Elgg rejected this request because the CSRF token is <strong>invalid or missing</strong>.<br>
      Your token defense is active and working correctly.
    </p>
    <p>Here is your Task 4 flag:</p>
    <div class="flag"><?= htmlspecialchars($flag) ?></div>
    <p style="margin-top:24px; font-size:0.85em;">
      Submit this flag in CyberRangeCZ to claim your 4 points.
    </p>
  </div>
</body>
</html>
