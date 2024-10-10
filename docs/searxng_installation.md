## Searxng installation guide

1. sudo apt install python3.10-venv
2. `git clone https://github.com/searxng/searxng && cd searxng`
2. Create a venv = `python3 -m venv searxng_env`
3. Activate env: `source searxng_env/bin/activate`
4. Modify `searx/settings.yml` add `- json` in `formats:`
5. sudo chmod 666 /var/run/docker.sock 
6. make docker.build
7. Docker run —rm -d -p 32768:8080 -v “@{PWD}/searxng:/etc/searxng” -e “BASE_URL=http://localhost$PORT” -e “INSTANCE_NAME=local_search” searxng/searxng

## Perplexica installation

1. git clone https://github.com/ItzCrazyKns/Perplexica.git && cd Perplexica
2. cp sample.config.toml config.toml
3. Add keys or endpoint to config.toml
4. sudo chmod 666 /var/run/docker.sock 
5. 
