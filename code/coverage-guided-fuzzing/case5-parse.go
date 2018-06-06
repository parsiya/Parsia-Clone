case 5:
    ipDollar = ipS[ippt-3 : ippt+1]
    //line ip.y:54
    {
        mask := net.CIDRMask(int(ipDollar[3].num), 32)
        min := ipDollar[1].addrRange.Min.Mask(mask)
        maxInt := binary.BigEndian.Uint32([]byte(min)) + // <---- panic here
            0xffffffff -
            binary.BigEndian.Uint32([]byte(mask)) // <---- panic here
        maxBytes := make([]byte, 4)
        binary.BigEndian.PutUint32(maxBytes, maxInt)
        maxBytes = maxBytes[len(maxBytes)-4:]
        max := net.IP(maxBytes)
        ipVAL.addrRange = AddressRange{
            Min: min.To4(),
            Max: max.To4(),
        }
    }