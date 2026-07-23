from PIL import Image, ImageSequence

input_file = "chick-run.gif"
output_file = "chick-run-hd.gif"

img = Image.open(input_file)

frames = []

for frame in ImageSequence.Iterator(img):

    frame = frame.convert("RGBA")

    # 3x pixel-perfect upscale
    frame = frame.resize(
        (1200, 255),
        Image.Resampling.NEAREST
    )

    frames.append(frame)

frames[0].save(
    output_file,
    save_all=True,
    append_images=frames[1:],
    duration=img.info.get("duration", 100),
    loop=0,
    disposal=2
)

print("DONE → chick-run-hd.gif")
