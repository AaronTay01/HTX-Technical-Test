# Project Title

Test Flask ping API response
python ping_api.py
curl http://127.0.0.1:8001/ping

Test Asr_api response
python asr_api.py
curl -F "files=@D:\Projects\HTX-Technical-Test\asr\sample-4.mp3" http://localhost:8001/asr


curl -X POST http://localhost:8001/asr -F "D:\Projects\HTX-Technical-Test\asr\sample-4.mp3"