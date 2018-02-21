import subprocess
content_types = {
  "text": "text/plain",
  "html": "text/html",
  "octet": "application/octet-stream",
  "xml": "application/xml",
  "form": "multipart/form-data",
  "json": "application/json",
}

user_agents = {
  "chrome-mac":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
  "chrome-win":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
  "IE11":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
  "IE10":"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
  "safari7":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
  "edge":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
}
def curl(url, options=[], request="GET", content_type="text", id="", pw="", token="", agent="", body="",
         referer="", accept="", accept_encoding="",accept_language="", cookie=""):
  response_ = {}
  request_ = {}
  logs_ = []
  code_ = 0
  opt = ["curl", "-ss", "-v", "-X", request.upper(), "-H", "Content-Type: %s" % content_types[content_type]]
  if len(token) > 0:
    opt += ["-H", "Authorization: %s" %(token)]
  elif len(id) > 0:
    opt += ["-u", "%s:%s" % (id, pw)]
  if len(body) > 0:
    opt += ["--data-binary", body]
  if len(agent) > 0:
    if agent in user_agents.keys():
      opt += ["-H", "user-agent: %s" % user_agents[agents]]
    else:
      opt += ["-H", "user-agent: %s" % agents]
  if len(referer) > 0:
    opt += ["-H", "referer: %s" % referer]
  if len(accept) > 0:
    opt += ["-H", "accept: %s" % accept]
  if len(cookie) > 0:
    opt += ["-H", "cookie: %s" % cookie]
  if len(accept_encoding) > 0:
    opt += ["-H", "accept-encoding: %s" % accept_encoding]
  if len(accept_language) > 0:
    opt += ["-H", "accept-language: %s" % accept_language]
  opt += options + [url,]
  res = subprocess.Popen(opt, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = res.communicate()
  err = err.splitlines()
  for i in err:
    if i[0] == "<":
      i = i[2:]
      if len(i.strip()) == 0:
        continue
      if len(i.split(":")) == 1:
        code_ = int(i.split()[1])
      else:
        j = i.split(":")
        response_[j[0]] = j[1].strip()
    elif i[0] == ">":
      i = i[2:]
      if len(i.strip()) == 0:
        continue
      j = i.split(":",1)
      if len(j) > 1:
        request_[j[0]] = j[1].strip()
    elif i[0] == "*":
      logs_.append(i[2:].strip())
  return {"code":code_, "logs":logs_, "request":request_, "response": response_, "body":out}

####// Example


import json
req = {"metadata": {"public": "true", "auto_scan": "true"}}
body = json.dumps(req)
url = "https://registry.harbor.com/api/projects/1"
res = curl(url, request="PUT", content_type="json", id="login_id", pw="login_pw", body=body)
print res["code"]
print res["body"]
    
