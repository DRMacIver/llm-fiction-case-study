import json

from tools.sources import SourceConfig, load_source, load_sources


def test_real_sources_json_has_autoroad_and_meta():
    sources = load_sources()
    assert set(sources) == {"autoroad", "meta"}
    assert sources["autoroad"].profile == "full"
    assert sources["autoroad"].premise_cutoff is True
    assert sources["autoroad"].keep_file_contents is True
    assert sources["meta"].profile == "meta"
    assert sources["meta"].premise_cutoff is False
    assert sources["meta"].keep_file_contents is False
    assert "hegel" in sources["meta"].anonymize
    assert sources["meta"].anonymize_placeholder == "«OTHER-PROJECT»"


def test_load_source_unknown_name_raises():
    try:
        load_source("nonexistent")
        assert False, "expected KeyError"
    except KeyError:
        pass


def test_load_sources_expands_paths_and_wires_dirs(tmp_path):
    cfg_path = tmp_path / "sources.json"
    cfg_path.write_text(
        json.dumps(
            {
                "sources": {
                    "demo": {
                        "transcripts_dir": "~/.claude/projects/-demo",
                        "repo_root": "/Users/x/Projects/demo",
                        "out_dir": "build/demo",
                        "site_dir": "site/src/demo/transcripts",
                        "summary_marker": "  - [Demo](demo/transcripts/index.md)",
                        "summary_prefix": "  ",
                        "profile": "meta",
                        "premise_cutoff": False,
                        "keep_file_contents": False,
                        "anonymize": ["widget"],
                    }
                }
            }
        )
    )
    sources = load_sources(cfg_path)
    demo = sources["demo"]
    assert isinstance(demo, SourceConfig)
    assert str(demo.transcripts_dir).startswith(str(demo.transcripts_dir.expanduser()))
    assert not str(demo.transcripts_dir).startswith("~")
    assert demo.parsed_dir.name == "parsed"
    assert demo.redacted_dir.name == "redacted"
    assert demo.parsed_dir.parent == demo.out_dir
    assert demo.anonymize == ["widget"]
