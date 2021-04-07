转载自[https://www.jianshu.com/p/784bd5eae452](https://www.jianshu.com/p/784bd5eae452)，特此表示感谢。

为了防止文章没了，我这里抄一份做备份~

# 解决办法：

使用“管理员身份”运行命令提示符/Windows PowerShell1.定位到office的安装目录cd 绝对路径

例如：
```
PS C:\Windows\system32> cd 'C:\Program Files\Microsoft Office\Office15'
PS C:\Program Files\Microsoft Office\Office15>
```
2.查询版本

cscript OSPP.VBS /dstatusPS

```
 C:\Program Files\Microsoft Office\Office15> cscript OSPP.VBS /dstatus
```

Microsoft (R) Windows Script Host Version 5.812版权所有(C) Microsoft Corporation。保留所有权利。---Processing-----------------------------------------------------------------SKU ID: ？？？？？-？？？？？-？？？？？-？？？？？LICENSE NAME: Office 15, OfficeProPlusVL_KMS_Client edition（具体版本）LICENSE DESCRIPTION: Office 15, VOLUME_KMSCLIENT channel（RETAIL为零售版，VOLUME为批量授权）BETA EXPIRATION: 1601/1/1LICENSE STATUS:  ---LICENSED---REMAINING GRACE: 179 days  (258131 minute(s) before expiring)（序列号有效期剩余天数）Last 5 characters of installed product key: GVGXT（这个是激活码的后五位, 重点在这里, 这个序列号有效，须保留)Activation Type Configuration: ALL        DNS auto-discovery: KMS name not available        KMS machine registry override defined: 10.3.0.2:1688        Activation Interval: 120 minutes        Renewal Interval: 10080 minutes        KMS host caching: Enabled------------------------------------------------------------------------------PRODUCT ID: ？？？？？-？？？？？-？？？？？-？？？？？SKU ID: ？？？LICENSE NAME: Office 16, Office16ProPlusR_Grace edition（具体版本）LICENSE DESCRIPTION: Office 16, RETAIL(Grace) channel （Retail为零售版，VL为批量授权）BETA EXPIRATION: 1601/1/1LICENSE STATUS: ---NOTIFICATIONS---ERROR CODE: 0xC004F009ERROR DESCRIPTION: The Software Licensing Service reported that the grace period expired.Last 5 characters of installed product key: BTDRB （这个是无效序列号激活码的后五位，需删除的是这个）---------------------------------------------------------------------------------Exiting-----------------------------

3.当出现多个版本时，删除无效的序列号

cscript ospp.vbs /unpkey:XXXXX(XXXXX代表已安装序列号的最后五位字符)

例如：
```
PS C:\Program Files\Microsoft Office\Office15> cscript ospp.vbs /unpkey:BTDRB
```

# 添加key

如果要添加某个key，cscript OSPP.VBS /inpkey:9RN4T-JPBQV-XQMC9-PM9FP-PGWP9

这些是长期有效的密钥，如果不行的话估计你就只能用破解版的了。祝你成功。
9RN4T-JPBQV-XQMC9-PM9FP-PGWP9 
TKX7J-VDN26-Y2WKQ-7MG8R-X2CC9 
N9M8X-QDKGK-W27Q6-2GQYT-TJC9K 
4VNXV-F7PBY-GY8WK-2KYDD-B96YQ 
HDN2D-VJPHH-D4P4K-BQ27R-BY28K 
Office 2013 Pro Plus MSDN Retail Keys:
NFFT2-HWVWR-C934T-YM2VJ-YPXKK 
THN7X-Y9DM4-QH2TT-XQ82G-9KVTX 
N9JFJ-44VW2-X3J33-BXX9K-P3429 
MJN6F-M8XD9-R84JM-P8P8W-J8C9K 
GW6J7-PXNRV-RDX9M-FFMFD-PYQ6X 
MG9FH-NXW9Y-HPKH8-VX786-WW9KK 
PNQ3K-3TD86-FPWY6-28BBT-D3TXK 
3GH3B-WN8RD-44QMH-2C86F-KBQ6X 
BGDVN-Y9R8K-PWQWH-38K8P-VFP9K 
B9GN2-DXXQC-9DHKT-GGWCR-4X6XK 
6PMNJ-Q33T3-VJQFJ-23D3H-6XVTX 
KDVQM-HMNFJ-P9PJX-96HDF-DJYGX 
366NX-BQ62X-PQT9G-GPX4H-VT7TX 
4HNBK-863MH-6CR6P-GQ6WP-J42C9 
6KTFN-PQH9H T8MMB-YG8K4-367TX 
KBDNM-R8CD9-RK366-WFM3X-C7GXK 
MH2KN-96KYR-GTRD4-KBKP4-Q9JP9 
2MNJP-QY9KX-MKBKM-9VFJ2-CJ9KK 
N4M7D-PD46X-TJ2HQ-RPDD7-T28P9 
NK8R7-8VXCQ 3M2FM-8446R-WFD6X 
2B8KN-FFK6J-YWMV4-J3DY2-3YF29 
MTDNG-PDDGD-MHMV4-F2MBY-RCXKK 
PBTFM-WWN3H-2GD9X-VJRMG-C9VTX 
G9N3P-GRJK6-VM63J-F9M27-KHGXK 
DMXHM-GNMM3-MYHHK-6TVT2-XTKKK 
GYWDG-NMV9P-746HR-Y2VQW-YPXKK 
6HDB9-BNRGY-J3F83-CF43C-D67TX 
X2YWD-NWJ42-3PGD6-M37DP-VFP9K 
GPT9W-CWNJK-KB29G-8V93J-TQ429 
46DNX-B4Q98-PQVPW-Q8VM6-FVR29 
PNP4F-KY64B-JJF4P-7R7J9-7XJP9 
WTFN9-KRCBV-2VBBH-BC272-27GXM 
N2P94-XV8HD-W9MHF-VQHHH-M4D6X 
433NF-H7TMK-TPMPK-W4FGW-7FP9K 
7TPNM-PMWKF-WVHKV-G869H-9BQ6X 
XRNFT-HG2FV-G74BP-7PVDC-JB29K 
DJC4N-DX7PC-GM3GK-V8KKW-XWYGX 
N7PXY-WR4XP-D4FGK-K66JH-CYQ6X 
XRNFT-HG2FV-G74BP-7PVDC-JB29K


