from typing import override

from enums.SendMode import SendMode
from utils.ExchangeKeyUtil import Curve,Sm2KeyAgreement
from gmssl.sm3 import sm3_kdf
from gmssl import func,sm3

from soft.AbsSoft import AbsSoft
import utils.ExchangeKeyUtil

class PublicKeySendSoft(AbsSoft):
    def __init__(self, tcp):
        self.tcp = tcp

    @override
    def run(self, **kwargs):
        # 明文手机号
        user_phone = kwargs["user_phone"]
        # 生成手机号的哈希值
        hash_user_phone = sm3.sm3_hash(func.bytes_to_list(user_phone.encode('utf-8')))
        self.tcp.hash_user_phone = hash_user_phone
        # 生成用户身份标识和长度标识
        id_entl_a = utils.ExchangeKeyUtil.calculate_id_and_entl(hash_user_phone)
        curve = Curve()
        user_a = Sm2KeyAgreement(curve, id_entl_a[0], id_entl_a[1])
        # 生成静态公钥和临时公钥 身份认证码
        p_a = user_a.curve.dot_to_bytes(user_a.pre_pub_key)
        r_a = user_a.curve.dot_to_bytes(user_a.tem_pub_key)
        z_a = user_a.id_auth_code
        user_a_data = {
            "user_a": user_a,
            "z_a": z_a,
        }
        send_data = {
            "data": {
                "p_a": p_a,
                "r_a": r_a,
                "z_a": z_a,
                "user_phone": hash_user_phone
            },
            "type": "negotiate_key"
        }
        self.tcp.send_msg(send_data,SendMode.UN_ENCRYPT)
        return user_a_data

class PublicKeyReceiveSoft(AbsSoft):
    def __init__(self, tcp):
        self.tcp = tcp

    @override
    def run(self, **kwargs):
        user_b_data = kwargs["user_b_data"]
        p_b = user_b_data["p_b"]
        r_b = user_b_data["r_b"]
        z_b = user_b_data["z_b"]
        # 使用服务器的临时公钥和静态公钥计算出协商点坐标 xy
        v_x, v_y = self.tcp.user_a_data["user_a"].key_adgreement(p_b, r_b)
        # 生成共享密钥
        k_a = sm3_kdf((v_x + v_y + self.tcp.user_a_data["z_a"] + z_b).encode(), self.tcp.user_a_data["user_a"].klen)
        return k_a