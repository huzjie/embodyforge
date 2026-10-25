.PHONY: test doctor bench train demo

test:
	python -m unittest discover -s tests -t .

doctor:
	python -m embodyforge doctor

bench:
	python -m embodyforge bench

train:
	python -m embodyforge train

demo:
	python -m embodyforge demo
