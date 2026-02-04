# 从项目根目录以模块方式启动客户端（避免 No module named 'rm_client'）
Set-Location $PSScriptRoot
python -m rm_client.main
