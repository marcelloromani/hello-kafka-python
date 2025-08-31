from click.testing import CliRunner

from hello_kafka_python.main import main


class TestMainBasicOptions:

    def test_should_support_help_option(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert len(result.output.strip()) > 0
