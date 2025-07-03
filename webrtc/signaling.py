import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription

class WebRTCSignaling:
    def __init__(self):
        self.connections = {}

    async def process_offer(self, offer_sdp, offer_type, connection_id):
        pc = RTCPeerConnection()
        self.connections[connection_id] = pc
        offer = RTCSessionDescription(sdp=offer_sdp, type=offer_type)
        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return pc.localDescription.sdp, pc.localDescription.type

    async def add_ice_candidate(self, connection_id, candidate):
        pc = self.connections.get(connection_id)
        if pc and candidate:
            await pc.addIceCandidate(candidate)

    def get_connection(self, connection_id):
        return self.connections.get(connection_id)

    def close_connection(self, connection_id):
        pc = self.connections.pop(connection_id, None)
        if pc:
            asyncio.ensure_future(pc.close())

# Example usage:
# signaling = WebRTCSignaling()
# sdp, type = await signaling.process_offer(offer_sdp, offer_type, connection_id)
# await signaling.add_ice_candidate(connection_id, candidate)
# signaling.close_connection(connection_id)
