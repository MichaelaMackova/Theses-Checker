#----------------------------------------------------------------------------
# File          : dailyDeleteFiles.ps1
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 03.12.2024
# Last Updated  : 03.12.2024
# License       : AGPL-3.0 license
#
# Description: 
#    Deletes PDF files in "files/" or "static/" folder and JSON files
#    in "files/json/" folder that are older than Period.
# ---------------------------------------------------------------------------


$TWO_HOURS_IN_SEC = 7200
$TWELVE_HOURS_IN_SEC = 43200
$DAY_IN_SEC = 86400
$THREE_DAYS_IN_SEC = 259200
$WEEK_IN_SEC = 604800


$Period = $TWELVE_HOURS_IN_SEC


$today = Get-Date
$time_to_delete = $today.AddSeconds(-$Period)

$files = Get-ChildItem -Path ./static/*.pdf, ./files/*.pdf, ./files/json/*.json -File | Where-Object { $_.LastWriteTime -lt $time_to_delete }
if ($files -ne $null) {
    Remove-Item -Path $files 
}