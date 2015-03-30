GEN_DIR=pb
PROTO_DIR=../../common/proto

NET_RPC_CS=$(PROTO_DIR)/client.protolist

NET_RPC_CS_HRL=$(GEN_DIR)/client_rpc.py

RPCC=lua gen_proto.lua 

.PHONY: all proto protolist clean

all: proto protolist

clean:
	-rm -r $(GEN_DIR) 
	find . -name "*.pyc" -exec rm {} \;

$(NET_RPC_CS_HRL):$(NET_RPC_CS)
	$(RPCC) $< $@ client

proto:
	-mkdir -p $(GEN_DIR)
	protoc --python_out=$(GEN_DIR) -I$(PROTO_DIR) `find $(PROTO_DIR) -name "*.proto"`
	find $(GEN_DIR) -type d -exec touch {}/__init__.py \;

protolist: $(NET_RPC_CS_HRL)

