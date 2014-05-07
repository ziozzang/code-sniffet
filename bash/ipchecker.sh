#!/bin/bash
# Heartbeat 에 따라서 IP가 변경되는것을 감지 하여, 다른 IP를 할당.
# 해당 머신에 CHECK_VIP 가 할당 되는 순간 TARGET_VIP를 같이 할당.
# 해당 머신에 CHECK_VIP 가 제거 되는 순간 TARGET_VIP를 같이 제거.
# - code by ziozzang@gmail.com

CHECK_VIP="1.2.3.4"
TARGET_VIP="1.2.3.5|1.2.3.6"
TARGET_DEV="eth0"
TMP_DIRS="/tmp/"

checkip() {
  local ip="$1"
  cnt=`ip addr | grep "${ip}" | wc -l`
  if [[ "${cnt}" -gt "0" ]]; then
    return 1
  else
    return 0
  fi
}

# 임시 파일을 만듬.
while IFS='|' read -ra ADDR; do
  for i in "${ADDR[@]}"; do
    rm -f "${TMP_DIRS}/${i}"
    checkip "${i}"
    if [[ "$?" -eq "1" ]]; then
      touch "${TMP_DIRS}/${i}"
      echo "ip set: ${i}"
    else
      echo "not set: ${i}"
    fi
  done
done <<< "${TARGET_VIP}"

# 루프로 동작
while :
do
  checkip "${CHECK_VIP}"
  FLAG_VIP=$?

  # 일단 IP를 바인딩 하자...
  while IFS='|' read -ra ADDR; do
    for i in "${ADDR[@]}"; do
      if [[ "${FLAG_VIP}" -eq "0" ]]; then
        if [[ -f "${TMP_DIRS}/${i}" ]]; then
          rm -f "${TMP_DIRS}/${i}"
          ip addr del ${i}/24 dev ${TARGET_DEV}
        fi
      else
        if [[ ! -f "${TMP_DIRS}/${i}" ]]; then
          touch "${TMP_DIRS}/${i}"
          ip addr add ${i}/24 dev ${TARGET_DEV}
        fi
      fi
    done
  done <<< "${TARGET_VIP}"

  sleep 1
done
