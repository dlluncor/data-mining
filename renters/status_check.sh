#echo '52.89.84.183 no_crosses'
#ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.89.84.183 'ps aux | grep [r]uby; tail data-mining/renters/data/out_no_0921212303.log | grep HITTING'
echo '52.89.130.208 full_crosses_0'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.89.130.208 'ps aux | grep [r]uby ; tail data-mining/renters/data/out_full_0_0921212303.log | grep HITTING'
echo '52.88.213.154 full_crosses_1'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.88.213.154 'ps aux | grep [r]uby; tail data-mining/renters/data/out_full_1_0921212303.log | grep HITTING'
echo '52.89.136.97 full_crosses_2'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.89.136.97 'ps aux | grep [r]uby; tail data-mining/renters/out_full_2_0921212303.log | grep HITTING'
echo '52.11.249.176 full_crosses_3'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.11.249.176 'ps aux | grep [r]uby; tail data-mining/renters/data/out_full_3_0921212303.log | grep HITTING'
echo '52.89.169.220 full_crosses_4'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.89.169.220 'ps aux | grep [r]uby; tail data-mining/renters/data/out_full_4_0921212303.log | grep HITTING'
echo '52.26.146.251 full_crosses_5'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.26.146.251 'ps aux | grep [r]uby; tail data-mining/renters/data/out_full_5_0921212303.log | grep HITTING'
echo '52.89.147.43 full_crosses_6'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.89.147.43 'ps aux | grep [r]uby; tail data-mining/renters/data/out_full_6_0921212303.log | grep HITTING'
echo '52.25.4.192 full_crosses_7'
ssh  -i ~/.ssh/bonjoy-team.pem ubuntu@52.25.4.192 'ps aux | grep [r]uby; tail data-mining/renters/data/out_full_7_0921212303.log | grep HITTING'
