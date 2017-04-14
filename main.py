from src.string_to_hash import Hash64

if __name__ == "__main__":

    hash_generator = Hash64()
    print(list(hash_generator.string_to_64hash("All work and no play made Hossein a dull boy")))
    print(list(hash_generator.string_to_64hash("All work and no play made Hossein a dull boy / ")))

