/**
 * Receipt resource API calls — mirrors routes/receipt.py (OCR upload).
 */
import { Receipt } from "../../common/types";
import { ReceiptSchema } from "../../common/validation";
import { apiClient } from "./client";

export async function uploadReceipt(imageUri: string): Promise<Receipt> {
  const formData = new FormData();
  formData.append("file", {
    uri: imageUri,
    name: "receipt.jpg",
    type: "image/jpeg",
  } as unknown as Blob);

  const { data } = await apiClient.post("/receipt/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return ReceiptSchema.parse(data);
}
