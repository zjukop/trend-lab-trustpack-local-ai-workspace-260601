from trustpack.main import cli, risk_score


def test_smoke_risk_score_blocks_risky():
    assert risk_score("rm -rf /tmp/x") >= 30


def test_smoke_cli_ask():
    code = cli(["ask", "hello"])
    assert code == 0
