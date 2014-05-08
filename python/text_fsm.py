dev = textfsm.TextFSM(open("./specparser/spec.device.tmpl","r")).ParseText("\n".join(ks["DEVICE"]))
for i in dev:
  r = {}
  r["host"] = i[0]
  r["pool"] = i[1]
  res["device"].append(r)


"""
Value Filldown DevHost (\S+)
Value Required DevPool (\S+)

Start
  # Device Info
  ^DEVICE\s+\"${DevHost}\"
  ^\s+-pool\s+\"${DevPool}\" -> Record
  # textfsm.TextFSM(open("spec.device.tmpl","r")).ParseText("\n".join(d["DEVICE"]))

"""
