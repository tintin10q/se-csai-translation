from onmt.bin.server import main


if __name__ == "__main__":
    main()


def start_model_server() -> None:
    """Function that will start the model/translation server"""
    main()
    print("started model server")
