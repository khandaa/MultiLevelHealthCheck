# # Test API 1 health
curl http://127.0.0.1:9001/api1/health

# Test API 2 health
curl http://127.0.0.1:9002/api2/health

# # Test API 3 health
curl http://127.0.0.1:9003/api3/health

# # Test API 4 health
curl http://127.0.0.1:9004/api4/health

# # Test overall healthcheck
curl http://127.0.0.1:8000/healthcheck
