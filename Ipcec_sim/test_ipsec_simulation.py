from ipsec_simulation import AntiReplayWindow, build_transport_packet, build_tunnel_packet


def test_transport_packet_includes_ipsec_headers():
    packet = build_transport_packet(
        src_ip="10.0.0.2",
        dst_ip="10.0.0.3",
        payload="PING",
        spi=0x1111,
        seq_no=7,
        protocol="ESP",
    )

    assert packet["mode"] == "transport"
    assert packet["header"]["proto"] == "ESP"
    assert packet["header"]["spi"] == 0x1111
    assert packet["header"]["sequence_number"] == 7
    assert packet["payload"] == "PING"


def test_tunnel_packet_wraps_inner_ip_and_outer_ip():
    packet = build_tunnel_packet(
        src_ip="192.168.1.10",
        dst_ip="192.168.1.20",
        inner_src="10.0.0.2",
        inner_dst="10.0.0.3",
        payload="SECRET",
        spi=0x2222,
        seq_no=3,
        protocol="AH",
    )

    assert packet["mode"] == "tunnel"
    assert packet["outer_ip"]["src"] == "192.168.1.10"
    assert packet["outer_ip"]["dst"] == "192.168.1.20"
    assert packet["inner_ip"]["src"] == "10.0.0.2"
    assert packet["inner_ip"]["dst"] == "10.0.0.3"
    assert packet["payload"] == "SECRET"


def test_replay_window_rejects_duplicates_and_old_packets():
    window = AntiReplayWindow(size=4)

    assert window.accept(10) is True
    assert window.accept(10) is False
    assert window.accept(11) is True
    assert window.accept(12) is True
    assert window.accept(9) is False
    assert window.accept(13) is True
