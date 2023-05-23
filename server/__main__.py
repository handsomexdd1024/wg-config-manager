import app
import config

if __name__ == "__main__":
    cfg = config.Config("config.yaml")
    app.run(cfg.listen_address, cfg.listen_port)