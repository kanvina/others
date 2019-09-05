// GeoHash: Encoding Latitude, Longitude based on Precison

function encodeGeoHash(lat, long, precision) 
{
  let latRange = [-90, 90];
  let longRange = [-180, 180];
  let stringBuilder = '';
  const base32Chars = '0123456789bcdefghjkmnpqrstuvwxyz';

  function getEncodeString(target, range) {
    let encodeString = '';
    let i = 0;
    while (i < 5 * 6) {
      if (target <= (range[0] + range[1]) / 2 && target >= range[0]) {
        encodeString += '0';
        range[1] = (range[0] + range[1]) / 2;
      } else {
        encodeString += '1';
        range[0] = (range[0] + range[1]) / 2;
      }
      i++;
    }
    return encodeString;
  }

  function mergeString(latString, longString) {
    let mergeString = '';
    for (let i = 0; i < longString.length; i++) {
      mergeString += longString[i];
      mergeString += latString[i];
    }

    for (let i = 0; i < mergeString.length; i += 5) {
      stringBuilder += base32Chars[parseInt(mergeString.substring(i, i + 5), 2)];
    }
  }

  let latString = getEncodeString(lat, latRange);
  let longString = getEncodeString(long, longRange);
  mergeString(latString, longString);
  return stringBuilder.substring(0, precision);
}

// Hashstring to Lat, Long

function decodeGeoHash(hashString) {
  let latRange = [-90, 90];
  let longRange = [-180, 180];
  let stringBuilder = '';
  const base32Chars = '0123456789bcdefghjkmnpqrstuvwxyz';

  function hashToBinary(hashString) {
    let ret = '';
    for (let i = 0; i < hashString.length; i++) {
      let binaryStr = base32Chars.indexOf(hashString[i]).toString(2);
      if (binaryStr.length == 5) {
        ret = ret + binaryStr;
        continue;
      }
      if (binaryStr.length < 5) {
        binaryStr = '00000'.slice(0, 5 - binaryStr.length) + binaryStr;
        ret = ret + binaryStr;
      }
    }
    return ret;
  }

  function convertToLatLong(binaryStr) {
    let latStr = '',
      longStr = '',
      ret = [0, 0];
    for (let i = 0; i < binaryStr.length; i++) {
      if (i % 2 == 0) {
        longStr += binaryStr[i];
      } else {
        latStr += binaryStr[i];
      }
    }

    for (let i = 0; i < latStr.length; i++) {
      let temp = [0, 0];
      if (latStr[i] == 0) {
        latRange[1] = (latRange[0] + latRange[1]) / 2;
      }
      if (latStr[i] == 1) {
        latRange[0] = (latRange[0] + latRange[1]) / 2;
      }
    }
    ret[1] = (latRange[0] + latRange[1]) / 2;
    for (let i = 0; i < longStr.length; i++) {
      let temp = [0, 0];
      if (longStr[i] == 0) {
        longRange[1] = (longRange[0] + longRange[1]) / 2;
      }
      if (longStr[i] == 1) {
        longRange[0] = (longRange[0] + longRange[1]) / 2;
      }
    }
    ret[0] = (longRange[0] + longRange[1]) / 2;
    return ret;
  }
  const binaryStr = hashToBinary(hashString);
  const coordinates = convertToLatLong(binaryStr);
  return coordinates;
}

// Hashstring to BoundBox (minLat, minLong, maxLat, maxLong)

function decodeGeoHashBBox(hashString) {
  let latRange = [-90, 90];
  let longRange = [-180, 180];
  let stringBuilder = '';
  const base32Chars = '0123456789bcdefghjkmnpqrstuvwxyz';

  function hashToBinary(hashString) {
    let ret = '';
    for (let i = 0; i < hashString.length; i++) {
      let binaryStr = base32Chars.indexOf(hashString[i]).toString(2);
      if (binaryStr.length == 5) {
        ret = ret + binaryStr;
        continue;
      }
      if (binaryStr.length < 5) {
        binaryStr = '00000'.slice(0, 5 - binaryStr.length) + binaryStr;
        ret = ret + binaryStr;
      }
    }
    return ret;
  }

  function convertToBBox(binaryStr) {
    let latStr = '',
      longStr = '',
      ret = [0, 0, 0, 0];
    for (let i = 0; i < binaryStr.length; i++) {
      if (i % 2 == 0) {
        longStr += binaryStr[i];
      } else {
        latStr += binaryStr[i];
      }
    }

    for (let i = 0; i < latStr.length; i++) {
      let temp = [0, 0];
      if (latStr[i] == 0) {
        latRange[1] = (latRange[0] + latRange[1]) / 2;
      }
      if (latStr[i] == 1) {
        latRange[0] = (latRange[0] + latRange[1]) / 2;
      }
    }

    if (latRange[0] < latRange[1]) {
      ret[0] = latRange[0];
      ret[2] = latRange[1];
    } else {
      ret[0] = latRange[1];
      ret[2] = latRange[0];
    }

    for (let i = 0; i < longStr.length; i++) {
      let temp = [0, 0];
      if (longStr[i] == 0) {
        longRange[1] = (longRange[0] + longRange[1]) / 2;
      }
      if (longStr[i] == 1) {
        longRange[0] = (longRange[0] + longRange[1]) / 2;
      }
    }

    if (longRange[0] < longRange[1]) {
      ret[1] = longRange[0];
      ret[3] = longRange[1];
    } else {
      ret[1] = longRange[1];
      ret[3] = longRange[0];
    }

    return ret;
  }
  const binaryStr = hashToBinary(hashString);
  const bbox = convertToBBox(binaryStr);
  return bbox;
}

// test
// const hash = encodeGeoHash(36.778259, 119.417931, 12);
// console.log(hash);
// const coor = decodeGeoHash('wwscjrm2zkrh');
// console.log(coor);
// const bbox = decodeGeoHashBBox('wwscjrm2zkrh');
// console.log(bbox);