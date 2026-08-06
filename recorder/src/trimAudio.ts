/** Decode a recorded blob, trim start/end, and re-encode as WAV for upload. */

export type TrimRange = {
  startSec: number;
  endSec: number;
};

function writeString(view: DataView, offset: number, str: string) {
  for (let i = 0; i < str.length; i += 1) {
    view.setUint8(offset + i, str.charCodeAt(i));
  }
}

/** Encode an AudioBuffer as 16-bit PCM WAV. */
export function audioBufferToWav(buffer: AudioBuffer): Blob {
  const numChannels = buffer.numberOfChannels;
  const sampleRate = buffer.sampleRate;
  const bitDepth = 16;
  const samples = buffer.length;
  const blockAlign = (numChannels * bitDepth) / 8;
  const byteRate = sampleRate * blockAlign;
  const dataSize = samples * blockAlign;
  const arrayBuffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(arrayBuffer);

  writeString(view, 0, "RIFF");
  view.setUint32(4, 36 + dataSize, true);
  writeString(view, 8, "WAVE");
  writeString(view, 12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, byteRate, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, bitDepth, true);
  writeString(view, 36, "data");
  view.setUint32(40, dataSize, true);

  const channels: Float32Array[] = [];
  for (let c = 0; c < numChannels; c += 1) {
    channels.push(buffer.getChannelData(c));
  }

  let offset = 44;
  for (let i = 0; i < samples; i += 1) {
    for (let c = 0; c < numChannels; c += 1) {
      const sample = Math.max(-1, Math.min(1, channels[c][i]));
      view.setInt16(
        offset,
        sample < 0 ? sample * 0x8000 : sample * 0x7fff,
        true
      );
      offset += 2;
    }
  }

  return new Blob([arrayBuffer], { type: "audio/wav" });
}

export function sliceAudioBuffer(
  source: AudioBuffer,
  startSec: number,
  endSec: number
): AudioBuffer {
  const start = Math.max(0, Math.min(startSec, source.duration));
  const end = Math.max(start + 0.05, Math.min(endSec, source.duration));
  const sampleRate = source.sampleRate;
  const startFrame = Math.floor(start * sampleRate);
  const endFrame = Math.floor(end * sampleRate);
  const frameCount = Math.max(1, endFrame - startFrame);
  const ctx = new OfflineAudioContext(
    source.numberOfChannels,
    frameCount,
    sampleRate
  );
  const trimmed = ctx.createBuffer(
    source.numberOfChannels,
    frameCount,
    sampleRate
  );
  for (let c = 0; c < source.numberOfChannels; c += 1) {
    const input = source.getChannelData(c).subarray(startFrame, endFrame);
    trimmed.copyToChannel(input, c, 0);
  }
  return trimmed;
}

export async function decodeAudioBlob(blob: Blob): Promise<AudioBuffer> {
  const ctx = new AudioContext();
  try {
    const arrayBuffer = await blob.arrayBuffer();
    return await ctx.decodeAudioData(arrayBuffer.slice(0));
  } finally {
    await ctx.close().catch(() => undefined);
  }
}

export async function trimBlobToWav(
  blob: Blob,
  range: TrimRange
): Promise<{ blob: Blob; duration: number }> {
  const decoded = await decodeAudioBlob(blob);
  const trimmed = sliceAudioBuffer(decoded, range.startSec, range.endSec);
  return {
    blob: audioBufferToWav(trimmed),
    duration: trimmed.duration,
  };
}

export function formatClipTime(seconds: number) {
  if (!Number.isFinite(seconds) || seconds < 0) return "0:00.0";
  const m = Math.floor(seconds / 60);
  const s = seconds - m * 60;
  return `${m}:${s.toFixed(1).padStart(4, "0")}`;
}
