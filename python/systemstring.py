# 파이썬에서 유니코드 오류라면서 ascii디코더가 어쩌고 저쩌고 라고 떠들면..
# 소스에 다음을 복불해서 넣으면 된다.

import sys
reload(sys)
sys.setdefaultencoding( "UTF-8" )

"""
이건 소스코드에 유니코드가 있어서
# -*- coding: utf-8 -*-
붙여 주는거랑 다른거임.

이건 스트링 처리 하는 기본 인코딩을 바꿔주는것임... -ㅅ-...
"""