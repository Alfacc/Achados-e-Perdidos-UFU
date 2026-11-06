// Converte a resposta de erro do DRF em { fields: {campo: "msg"}, message: "msg geral" }.
export function parseApiError(err) {
  const data = err?.response?.data;
  if (!data || typeof data !== "object") {
    return { fields: {}, message: "Não foi possível conectar ao servidor. Tente novamente." };
  }
  if (data.detail) return { fields: {}, message: data.detail };

  const fields = {};
  for (const [key, value] of Object.entries(data)) {
    fields[key] = Array.isArray(value) ? value.join(" ") : String(value);
  }
  return { fields, message: "Corrija os campos destacados." };
}
