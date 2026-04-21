from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet

log = core.getLogger()

class TopologyDetector(object):

    def __init__(self):
        core.openflow.addListeners(self)
        log.info("🔥 Final Clean Controller Started")

    def _handle_ConnectionUp(self, event):
        log.info("🟢 Switch Connected: %s", event.connection.dpid)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        dpid = event.connection.dpid
        in_port = event.port

        # ---- SAFE PARSING (prevents DNS errors) ----
        if not packet or not isinstance(packet, ethernet):
            return

        # ---- LOG PACKET ----
        log.info("📦 Packet received at switch %s on port %s", dpid, in_port)

        # ---- ALLOW ONLY ARP + IPv4 ----
        if packet.type not in (0x0800, 0x0806):
            return

        # ---- HANDLE ARP ----
        if packet.type == 0x0806:
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            event.connection.send(msg)
            return

        msg = of.ofp_packet_out()
        msg.data = event.ofp

        # ---------- PRIMARY + BACKUP ----------

        # s1
        if dpid == 1:
            if in_port == 1:
                msg.actions.append(of.ofp_action_output(port=2))
                msg.actions.append(of.ofp_action_output(port=3))
            else:
                msg.actions.append(of.ofp_action_output(port=1))

        # s2
        elif dpid == 2:
            if in_port == 1:
                msg.actions.append(of.ofp_action_output(port=2))
                msg.actions.append(of.ofp_action_output(port=3))
            else:
                msg.actions.append(of.ofp_action_output(port=1))

        # s3
        elif dpid == 3:
            if in_port == 1:
                msg.actions.append(of.ofp_action_output(port=2))
            else:
                msg.actions.append(of.ofp_action_output(port=1))

        else:
            return

        event.connection.send(msg)

def launch():
    core.registerNew(TopologyDetector)
