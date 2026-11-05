
const API_BASE_URL = "/api/enterprise-services";


// ==========================================
// HTTP Request
// ==========================================

// 統一處理 HTTP Request 與 Response
async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      Accept: "application/json",
      ...options.headers,
    },
  });

  // HTTP Error Handling
  if (!response.ok) {
    let errorMessage = `Request failed (${response.status})`;

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      } else if (Array.isArray(errorData.detail)) {
        errorMessage = errorData.detail
          .map((item) => item.msg)
          .filter(Boolean)
          .join("; ");
      }
    } catch {
      // Response 不是 JSON 時，保留預設錯誤訊息
    }

    throw new Error(errorMessage);
  }

  // HTTP 204 No Content
  if (response.status === 204) {
    return null;
  }

  return response.json();
}


// ==========================================
// Enterprise Service API
// ==========================================

// 取得所有企業服務
export async function getEnterpriseServices() {
  const data = await request(API_BASE_URL);

  if (!Array.isArray(data)) {
    throw new Error("Invalid enterprise services response");
  }

  return data;
}


// 新增企業服務
export async function createEnterpriseService(serviceData) {
  return request(API_BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(serviceData),
  });
}


// 修改企業服務
export async function updateEnterpriseService(
  serviceId,
  serviceData,
) {
  return request(`${API_BASE_URL}/${serviceId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(serviceData),
  });
}


// 刪除企業服務
export async function deleteEnterpriseService(serviceId) {
  return request(`${API_BASE_URL}/${serviceId}`, {
    method: "DELETE",
  });
}
