# setup-nlm-scheduler.ps1 — Register daily auth check in Windows Task Scheduler

$taskName = "NotebookLM Auth Check"

# Remove existing task if present
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

$action = New-ScheduledTaskAction `
    -Execute "C:\Program Files\Git\bin\bash.exe" `
    -Argument "-c '$env:USERPROFILE/Documents/scripts/nlm-auth-check.sh'"

$trigger = New-ScheduledTaskTrigger -Daily -At "10:00AM"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Daily check of NotebookLM cookie authentication"

Write-Host "Task '$taskName' registered: runs daily at 10:00 AM"
