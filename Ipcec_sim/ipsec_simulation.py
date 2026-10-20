from __future__ import annotations


class AntiReplayWindow:


    def __init__(self, size: int = 32):
        if size <= 0:
            raise ValueError("El tamaño de la ventana debe ser mayor que cero.")

        self.size = size
        self.seen: set[int] = set()
        self.highest: int | None = None

    def accept(self, seq_no: int) -> bool:
        """Devuelve True si el paquete puede ser aceptado."""
        if seq_no in self.seen:
            return False

        if self.highest is None:
            self.highest = seq_no
            self.seen.add(seq_no)
            return True

        old_threshold = self.highest - self.size + 1
        if seq_no <= old_threshold:
            return False

        self.seen.add(seq_no)
        if seq_no > self.highest:
            self.highest = seq_no
        self.seen = {value for value in self.seen if value >= self.highest - self.size + 1}
        return True


def build_transport_packet(
    src_ip: str,
    dst_ip: str,
    payload: str,
    spi: int,
    seq_no: int,
    protocol: str = "ESP",
) -> dict:
    return {
        "mode": "transport",
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "header": {
            "proto": protocol,
            "spi": spi,
            "sequence_number": seq_no,
        },
        "payload": payload,
    }


def build_tunnel_packet(
    src_ip: str,
    dst_ip: str,
    inner_src: str,
    inner_dst: str,
    payload: str,
    spi: int,
    seq_no: int,
    protocol: str = "ESP",
) -> dict:
    
    return {
        "mode": "tunnel",
        "outer_ip": {"src": src_ip, "dst": dst_ip},
        "inner_ip": {"src": inner_src, "dst": inner_dst},
        "header": {
            "proto": protocol,
            "spi": spi,
            "sequence_number": seq_no,
        },
        "payload": payload,
    }


if __name__ == "__main__":
    window = AntiReplayWindow(size=4)
    packets = [10, 11, 12, 9, 13]

    for seq in packets:
        print(f"Secuencia {seq}: {'ACEPTADO' if window.accept(seq) else 'RECHAZADO'}")

    print("\nEjemplo transporte:")
    print(build_transport_packet("10.0.0.2", "10.0.0.3", "PING", 0x1111, 7, "ESP"))

    print("\nEjemplo túnel:")
    print(
        build_tunnel_packet(
            "192.168.1.10",
            "192.168.1.20",
            "10.0.0.2",
            "10.0.0.3",
            "SECRET",
            0x2222,
            3,
            "AH",
        )
    )
