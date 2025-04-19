import { IMGSERVE_BASE_URL } from './constants';
import { VN, Character, Release, VisualNovelDataBaseQueryResponse } from './types';

const IMAGE_REGEX = /^https?:\/\/[^\/]+\/(cv|sf|ch)(?:\.t)?\/\d+\/(\d+)\.jpg$/;

function convertToImgserveUrl(url?: string, thumbnail: boolean = false): string | undefined {
  if (!url) return undefined;
  
  const match = url.match(IMAGE_REGEX);
  if (!match) return url;

  const [, type, id] = match;
  const imageType = thumbnail ? `${type}.t` : type;
  return `${IMGSERVE_BASE_URL}/${imageType}/${id}`;
}

export function processVNImages(vn: VN): VN {
  return {
    ...vn,
    image: vn.image && {
      ...vn.image,
      url: convertToImgserveUrl(vn.image?.url),
      thumbnail: convertToImgserveUrl(vn.image?.thumbnail, true)
    },
    screenshots: vn.screenshots?.map(screenshot => ({
      ...screenshot,
      url: convertToImgserveUrl(screenshot?.url),
      thumbnail: convertToImgserveUrl(screenshot?.thumbnail, true)
    })),
  };
}

export function processCharacterImages(character: Character): Character {
  return {
    ...character,
    image: character.image && {
      ...character.image,
      url: convertToImgserveUrl(character.image?.url)
    }
  };
}

export function processReleaseImages(release: Release): Release {
  return {
    ...release,
    images: release.images?.map(image => ({
      ...image,
      url: convertToImgserveUrl(image?.url),
      thumbnail: convertToImgserveUrl(image?.thumbnail, true)
    }))
  };
}

export function processApiResponse<T extends VN | Character | Release>(
  response: VisualNovelDataBaseQueryResponse<T>,
  processor: (item: T) => T
): VisualNovelDataBaseQueryResponse<T> {
  return {
    ...response,
    results: response.results.map(processor)
  };
}