FFMPEG=./ffmpeg-0.6.1
FFMPEG_TAR=ffmpeg-0.6.1.tar.bz2
FFMPEG_OPTIONS= \
			--disable-doc \
			--disable-ffmpeg \
			--disable-ffplay \
			--disable-ffprobe \
			--disable-ffserver \
			--disable-network \
			--disable-avdevice \
			--disable-swscale \
			--enable-nonfree \
			--disable-everything \
			--enable-demuxer=mpegts \
			--enable-decoder=h264 \
			--enable-decoder=ac3 \
			--enable-decoder=pgssub \
			--enable-protocol=file

ZLIB=./zlib-1.2.8
ZLIB_TAR=zlib-1.2.8.tar.gz


all: $(ZLIB) $(FFMPEG)
	gcc -O3 -L$(FFMPEG)/libavdevice -L$(FFMPEG)/libavformat -L$(FFMPEG)/libavcodec -L$(FFMPEG)/libavutil -L$(ZLIB) -I$(FFMPEG) -o avchd2srt-core avchd2srt-core.c -lavutil -lavformat -lavcodec -lz -lavutil -lm

$(FFMPEG):
	tar xf $(FFMPEG_TAR)
	patch -p0 < ffserver.patch
	cd $(FFMPEG); ./configure $(FFMPEG_OPTIONS)
	make -C $(FFMPEG) -j 8

$(ZLIB):
	tar xf $(ZLIB_TAR)
	cd $(ZLIB); ./configure
	make -C $(ZLIB) -j 8
