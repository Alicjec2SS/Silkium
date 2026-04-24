# dns_seed_server.py
# pip install dnslib
#
# DNS Seed kiểu Bitcoin:
# Query domain seed.evenander.net -> trả random các peer đã từng join
#
# Chạy:
# python dns_seed_server.py
#
# Test:
# nslookup seed.evenander.net 127.0.0.1

import time
import random
from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, A, RCODE

# ========================
# CONFIG
# ========================

DOMAIN = "seed.ineedanewguitar.net."   # đổi domain cho đẹp
LISTEN_IP = "0.0.0.0"
PORT = 53

TTL = 60
PEER_TIMEOUT = 3600        # peer hết hạn sau 1 giờ
MAX_RETURN = 1             # trả tối đa 5 peer / query

# lưu peer
# peers[ip] = last_seen_timestamp
peers = {}


# ========================
# DNS Resolver
# ========================

class SeedResolver(BaseResolver):

    def cleanup(self):
        now = time.time()
        dead = []

        for ip, last in peers.items():
            if now - last > PEER_TIMEOUT:
                dead.append(ip)

        for ip in dead:
            del peers[ip]

    def resolve(self, request, handler):
        self.cleanup()

        reply = request.reply()

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        client_ip = handler.client_address[0]

        # chỉ xử lý A record + đúng domain
        if qname != DOMAIN or qtype != "A":
            reply.header.rcode = RCODE.NXDOMAIN
            return reply

        # peer vừa query => add/update
        peers[client_ip] = time.time()

        # chọn peer khác nó
        candidates = [ip for ip in peers if ip != client_ip]

        if not candidates:
            candidates = [client_ip]

        random.shuffle(candidates)

        selected = candidates[:MAX_RETURN]

        print(f"[JOIN] {client_ip}")
        print(f"[RETURN] {selected}")

        for ip in selected:
            reply.add_answer(
                RR(
                    DOMAIN,
                    QTYPE.A,
                    rdata=A(ip),
                    ttl=TTL
                )
            )

        return reply


# ========================
# MAIN
# ========================

if __name__ == "__main__":
    print("===================================")
    print(" DNS Seed Server Running")
    print(" Domain :", DOMAIN)
    print(" Port   :", PORT)
    print("===================================")

    server = DNSServer(
        SeedResolver(),
        port=PORT,
        address=LISTEN_IP
    )

    server.start()