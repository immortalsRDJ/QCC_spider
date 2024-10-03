## QCC_Spider 

#### Step1 Environment Setting

For first time users, run the code below in your local shell.

```bash
git clone https://github.com/immortalsRDJ/QCC_spider.git
cd QCC_spider

conda create -n QCC python=3.10
conda activate QCC
pip install -r requirements.txt
```

#### Step2 Cookie Getting

1. Log in https://www.qcc.com/

2. open "inspect" - "Network" - "www.qcc.com" - "Cookies" (If it's not working, try reloading)

3. Copy "QCCSESSID" and "qcc_did" to the code

4. Run

---

- ***main.py***: synchronous scraper 
- ***Layer3_spider.py***: asynchronous scraper which could get 3 layers of basic and shareholder in a row.

---

*Last update: Oct 2, 2024*
