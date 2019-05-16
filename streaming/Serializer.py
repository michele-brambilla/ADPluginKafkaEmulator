"""
Bla bla bla
"""

from __future__ import absolute_import, division, print_function

import numpy

try:
    import flatbuffers
    from streaming.hs00 import EventHistogram, Array, ArrayUInt, ArrayFloat
    from streaming.hs00 import ArrayDesc, DimensionMetaData

    uint32_bytes = flatbuffers.number_types.Uint32Flags.bytewidth
except ImportError:
    flatbuffers = None
    uint32_bytes = 4
    EventHistogram = None
    Array = None
    ArrayUInt = None
    ArrayFloat = None
    DimensionMetaData = None
    ArrayDesc = None


class HistogramFlatbuffersSerializer(object):
    """ Encode the histogram using the flatbuffers schema hs00
    """

    file_identifier = "hs00"
    uint32_bytes = uint32_bytes

    def _encodeMetadata(self, b, desc):
        # Serialize the metadatas for each dimensions
        dims = []
        for d in range(len(desc.shape)):
            pos_unit = 0
            if hasattr(desc, 'dimunits'):
                pos_unit = b.CreateString(desc.dimunits[d])

            pos_label = b.CreateString(desc.dimnames[d])

            pos_bin = 0
            if hasattr(desc, 'dimbins'):
                bins = desc.dimbins[d]
                # Write only if the number of bins = length + 1
                if len(bins) == desc.shape[d] + 1:
                    ArrayFloat.ArrayFloatStartValueVector(b, len(bins))
                    # Prepend the bins
                    for bin_ in bins[::-1]:
                        b.PrependFloat32(bin_)
                    pos_val = b.EndVector(len(bins))
                    ArrayFloat.ArrayFloatStart(b)
                    ArrayFloat.ArrayFloatAddValue(b, pos_val)
                    pos_bin = ArrayFloat.ArrayFloatEnd(b)

            DimensionMetaData.DimensionMetaDataStart(b)
            DimensionMetaData.DimensionMetaDataAddLength(b, desc.shape[d])
            DimensionMetaData.DimensionMetaDataAddLabel(b, pos_label)
            if pos_unit:
                DimensionMetaData.DimensionMetaDataAddUnit(b, pos_unit)
            if pos_bin:
                DimensionMetaData.DimensionMetaDataAddBinBoundaries(b, pos_bin)
                DimensionMetaData.DimensionMetaDataAddBinBoundariesType(
                    b, Array.Array.ArrayFloat)
            dims.append(DimensionMetaData.DimensionMetaDataEnd(b))
        return dims

    def _encodeArray(self, builder, array, l_elements):
        # Serialize the data array
        ArrayUInt.ArrayUIntStartValueVector(builder, l_elements)

        if not isinstance(array, bytearray):
            array = bytearray(array.flatten('C').astype('uint32'))

        # Directly copy the bytes array
        l_bytes = l_elements * self.uint32_bytes  # Number of bytes in hist

        # Recalculate the head position of the buffer
        head = flatbuffers.number_types.UOffsetTFlags.py_type(
            builder.Head() - l_bytes)
        builder.head = head

        # Copy the bytes from histogram bytearray
        builder.Bytes[head:head + l_bytes] = array[0:l_bytes]

        pos_val = builder.EndVector(l_elements)
        ArrayUInt.ArrayUIntStart(builder)
        ArrayUInt.ArrayUIntAddValue(builder, pos_val)
        return ArrayUInt.ArrayUIntEnd(builder)

    def encode(self, timestamp_ns, arraydesc, array, source, metadata_ts=0,
               infostr=''):
        """Serialize using provided argument
        :param timestamp_ns: timestamp in ns
        :param arraydesc: array desc object of the associated image array
        :param array: the data array (can be in bytes or uint32)
        :param source: source name string
        :param metadata_ts: timestamp when last metadata was dumped
                        (if 0, metadata is dumped with this message)
        :param infostr: additional information
        :return: encoded bytes
        """
        rank = len(arraydesc.shape)
        builder = flatbuffers.Builder(16)

        pos_source = builder.CreateString(source)

        pos_metadata = 0
        if metadata_ts == 0:
            metadata = self._encodeMetadata(builder, arraydesc)
            EventHistogram.EventHistogramStartDimMetadataVector(builder, rank)
            for dim in metadata[::-1]:
                builder.PrependUOffsetTRelative(dim)
            pos_metadata = builder.EndVector(rank)
            metadata_ts = timestamp_ns

        EventHistogram.EventHistogramStartCurrentShapeVector(builder, rank)
        for s in arraydesc.shape[::-1]:
            builder.PrependUint32(s)
        pos_shape = builder.EndVector(rank)

        pos_data = self._encodeArray(builder, array,
                                     numpy.prod(arraydesc.shape))

        pos_info = builder.CreateString(infostr)

        # BUILD THE BUFFER
        EventHistogram.EventHistogramStart(builder)
        EventHistogram.EventHistogramAddSource(builder, pos_source)
        EventHistogram.EventHistogramAddTimestamp(builder, timestamp_ns)
        if pos_metadata:
            EventHistogram.EventHistogramAddDimMetadata(builder, pos_metadata)
        EventHistogram.EventHistogramAddLastMetadataTimestamp(builder,
                                                              metadata_ts)
        EventHistogram.EventHistogramAddCurrentShape(builder, pos_shape)
        EventHistogram.EventHistogramAddData(builder, pos_data)
        EventHistogram.EventHistogramAddDataType(builder,
                                                 Array.Array.ArrayUInt)
        EventHistogram.EventHistogramAddInfo(builder, pos_info)
        hist = EventHistogram.EventHistogramEnd(builder)
        builder.Finish(hist)

        # Generate the output and replace the file_identifier
        buff = builder.Output()
        buff[4:8] = bytes(self.file_identifier.encode('utf-8'))
        return bytes(buff)
