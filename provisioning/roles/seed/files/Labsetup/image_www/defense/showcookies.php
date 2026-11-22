<?php
/**
 * SEED Lab Task 5 — SameSite Cookie Experiment
 *
 * Shows which cookies arrived with this request.
 * When the request comes from attacker32.com AND the SameSite-protected
 * cookies are absent (blocked by the browser on a cross-site POST),
 * the Task 5 flag is revealed.
 *
 * The flag is unique per sandbox, injected via the container .env file.
 */

$flag_t5    = getenv('FLAG_T5') ?: 'FLAG_T5_NOT_SET';
$from_attacker = isset($_SERVER['HTTP_REFERER']) &&
                 strpos($_SERVER['HTTP_REFERER'], 'attacker32.com') !== false;
$lax_blocked    = !isset($_COOKIE['cookie-lax']);
$strict_blocked = !isset($_COOKIE['cookie-strict']);
$show_flag      = $from_attacker && $lax_blocked && $strict_blocked;
?>
<html>
<head><title>SameSite Cookie Experiment</title></head>
<style>
body  { background:#D4EFDF; font-family:Arial,Helvetica,sans-serif; margin:40px; }
li    { color:blue; }
.flag { background:#1a2433; color:#4ade80; font-family:monospace;
        font-size:1.2em; padding:16px 24px; border-radius:6px;
        margin-top:16px; display:inline-block; }
.box  { background:#fff; border-radius:8px; padding:24px;
        margin-top:24px; border:2px solid #27ae60; }
</style>
<body>

<h1>Displaying All Cookies Sent by Browser</h1>
<ul>
<?php foreach ($_COOKIE as $key => $val): ?>
  <li><h3><?= htmlspecialchars($key) ?>=<?= htmlspecialchars($val) ?></h3></li>
<?php endforeach; ?>
</ul>

<h2>Your request is a <font color='red'>
<?php echo isset($_COOKIE['cookie-strict']) ? 'same-site' : 'cross-site'; ?>
</font> request!</h2>

<?php if ($show_flag): ?>
<div class="box">
  <h2 style="color:#27ae60;">&#x1F3C6; Task 5 Complete!</h2>
  <p>
    Request came from <strong>attacker32.com</strong> and both
    <code>cookie-lax</code> and <code>cookie-strict</code> were blocked by
    the browser's SameSite policy. This proves the defense works.
  </p>
  <p>Your flag:</p>
  <div class="flag"><?= htmlspecialchars($flag_t5) ?></div>
  <p style="margin-top:16px; color:#555; font-size:0.9em;">
    Submit this in CyberRangeCZ to claim your 4 points.
  </p>
</div>
<?php elseif ($from_attacker): ?>
<div style="background:#fef3c7; border-radius:8px; padding:16px; margin-top:16px; border:2px solid #f59e0b;">
  <b>Almost there.</b> Request came from attacker32.com but some SameSite cookies
  still arrived. Make sure you are using a <strong>POST form</strong> (not a GET link)
  to trigger the cross-site request.
</div>
<?php endif; ?>

</body>
</html>
