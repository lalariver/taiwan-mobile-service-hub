
import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  createEnterpriseService,
  deleteEnterpriseService,
  getEnterpriseServices,
  updateEnterpriseService,
} from "./services/api.js";


// ==========================================
// Constants
// ==========================================

const CATEGORY_OPTIONS = [
  {
    value: "connectivity",
    label: "Connectivity",
    description: "網路連線",
  },
  {
    value: "cloud_computing",
    label: "Cloud & Computing",
    description: "雲端與運算",
  },
  {
    value: "client_solutions_ai",
    label: "AI Solutions",
    description: "AI 與客戶解決方案",
  },
  {
    value: "cybersecurity",
    label: "Cybersecurity",
    description: "資訊安全",
  },
  {
    value: "carbon_energy",
    label: "Carbon & Energy",
    description: "碳管理與能源",
  },
  {
    value: "consulting_managed",
    label: "Consulting & Managed",
    description: "顧問與代管服務",
  },
];

const INITIAL_FORM_DATA = {
  code: "",
  name: "",
  category: "connectivity",
  description: "",
  is_active: true,
};


// ==========================================
// Utilities
// ==========================================

// 取得分類顯示名稱
function getCategoryLabel(category) {
  const option = CATEGORY_OPTIONS.find(
    (item) => item.value === category,
  );

  return option?.description ?? category;
}


// 格式化日期
function formatDate(value) {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat("zh-TW", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}


// ==========================================
// Main Application
// ==========================================

function App() {

  // ----------------------------------------
  // State
  // ----------------------------------------

  const [services, setServices] = useState([]);

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [error, setError] = useState("");

  const [searchTerm, setSearchTerm] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingService, setEditingService] = useState(null);

  const [formData, setFormData] = useState({
    ...INITIAL_FORM_DATA,
  });


  // ----------------------------------------
  // API
  // ----------------------------------------

  // 取得企業服務
  const loadServices = useCallback(async () => {
    setIsLoading(true);

    try {
      const data = await getEnterpriseServices();

      setServices(data);
      setError("");
    } catch (requestError) {
      setError(
        requestError.message || "無法取得企業服務資料",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);


  // 初次載入
  useEffect(() => {
    loadServices();
  }, [loadServices]);


  // ----------------------------------------
  // Computed Data
  // ----------------------------------------

  // 統計服務數量
  const statistics = useMemo(() => {
    const activeCount = services.filter(
      (service) => service.is_active,
    ).length;

    return {
      total: services.length,
      active: activeCount,
      inactive: services.length - activeCount,
    };
  }, [services]);


  // 搜尋與篩選
  const filteredServices = useMemo(() => {
    return services.filter((service) => {

      const keyword = searchTerm.trim().toLowerCase();

      const matchesSearch =
        !keyword ||
        service.name.toLowerCase().includes(keyword) ||
        service.code.toLowerCase().includes(keyword) ||
        service.description.toLowerCase().includes(keyword);

      const matchesCategory =
        categoryFilter === "all" ||
        service.category === categoryFilter;

      const matchesStatus =
        statusFilter === "all" ||
        (statusFilter === "active" && service.is_active) ||
        (statusFilter === "inactive" && !service.is_active);

      return (
        matchesSearch &&
        matchesCategory &&
        matchesStatus
      );
    });
  }, [
    services,
    searchTerm,
    categoryFilter,
    statusFilter,
  ]);


  // ----------------------------------------
  // Modal Actions
  // ----------------------------------------

  // 開啟新增視窗
  const openCreateModal = () => {
    setEditingService(null);

    setFormData({
      ...INITIAL_FORM_DATA,
    });

    setError("");
    setIsModalOpen(true);
  };


  // 開啟編輯視窗
  const openEditModal = (service) => {
    setEditingService(service);

    setFormData({
      code: service.code,
      name: service.name,
      category: service.category,
      description: service.description,
      is_active: service.is_active,
    });

    setError("");
    setIsModalOpen(true);
  };


  // 關閉視窗
  const closeModal = () => {
    setIsModalOpen(false);
    setEditingService(null);

    setFormData({
      ...INITIAL_FORM_DATA,
    });
  };


  // ----------------------------------------
  // Form Actions
  // ----------------------------------------

  // 更新表單
  const handleInputChange = (event) => {
    const { name, value, checked, type } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: type === "checkbox" ? checked : value,
    }));
  };


  // 新增或修改企業服務
  const handleSubmit = async (event) => {
    event.preventDefault();

    setIsSubmitting(true);
    setError("");

    const payload = {
      ...formData,
      code: formData.code.trim().toUpperCase(),
      name: formData.name.trim(),
      description: formData.description.trim(),
    };

    try {
      if (editingService) {
        await updateEnterpriseService(
          editingService.id,
          payload,
        );
      } else {
        await createEnterpriseService(payload);
      }

      closeModal();

      await loadServices();
    } catch (requestError) {
      setError(
        requestError.message || "儲存企業服務失敗",
      );
    } finally {
      setIsSubmitting(false);
    }
  };


  // ----------------------------------------
  // Service Actions
  // ----------------------------------------

  // 啟用或停用企業服務
  const handleToggleStatus = async (service) => {
    const payload = {
      code: service.code,
      name: service.name,
      category: service.category,
      description: service.description,
      is_active: !service.is_active,
    };

    try {
      setError("");

      await updateEnterpriseService(
        service.id,
        payload,
      );

      await loadServices();
    } catch (requestError) {
      setError(
        requestError.message || "更新服務狀態失敗",
      );
    }
  };


  // 刪除企業服務
  const handleDelete = async (service) => {
    const confirmed = window.confirm(
      `確定要刪除「${service.name}」嗎？`,
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      await deleteEnterpriseService(service.id);

      await loadServices();
    } catch (requestError) {
      setError(
        requestError.message || "刪除企業服務失敗",
      );
    }
  };


  // ========================================
  // Render
  // ========================================

  return (
    <div className="app-shell">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-logo">
            T
          </div>

          <div className="brand-info">
            <h1>Taiwan Mobile</h1>
            <span>Service Hub</span>
          </div>
        </div>


        <div className="sidebar-section">
          <span className="sidebar-label">
            WORKSPACE
          </span>

          <nav className="sidebar-nav">
            <button
              type="button"
              className="nav-item active"
            >
              <span>▦</span>
              企業服務管理
            </button>
          </nav>
        </div>


        <div className="sidebar-footer">
          <div className="user-avatar">
            A
          </div>

          <div>
            <strong>Administrator</strong>
            <span>Portfolio Demo</span>
          </div>
        </div>

      </aside>


      {/* Main Content */}
      <main className="main-content">

        {/* Header */}
        <header className="topbar">

          <div>
            <span className="breadcrumb">
              Workspace / Enterprise Services
            </span>

            <h2>企業服務管理</h2>
          </div>

          <div className="topbar-right">
            <span className="environment-badge">
              DEMO ENVIRONMENT
            </span>

            <div className="user-avatar">
              A
            </div>
          </div>

        </header>


        {/* Dashboard */}
        <section className="dashboard-content">

          <div className="page-heading">
            <div>
              <h3>服務總覽</h3>

              <p>
                管理企業服務項目、服務分類與啟用狀態。
              </p>
            </div>

            <button
              type="button"
              className="primary-button"
              onClick={openCreateModal}
            >
              + 新增服務
            </button>
          </div>


          {/* Error Message */}
          {error && !isModalOpen && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}


          {/* Statistics */}
          <div className="statistics-grid">

            <div className="stat-card">
              <span>服務總數</span>

              <strong>
                {statistics.total}
              </strong>

              <small>Enterprise Services</small>
            </div>


            <div className="stat-card">
              <span>啟用中</span>

              <strong className="stat-active">
                {statistics.active}
              </strong>

              <small>Active Services</small>
            </div>


            <div className="stat-card">
              <span>已停用</span>

              <strong className="stat-inactive">
                {statistics.inactive}
              </strong>

              <small>Inactive Services</small>
            </div>

          </div>


          {/* Service List */}
          <section className="service-section">

            <div className="section-heading">
              <div>
                <h3>企業服務目錄</h3>

                <span>
                  共 {filteredServices.length} 項服務
                </span>
              </div>
            </div>


            {/* Filters */}
            <div className="filter-toolbar">

              <div className="search-box">
                <span>⌕</span>

                <input
                  type="search"
                  placeholder="搜尋服務名稱、代碼或說明..."
                  value={searchTerm}
                  onChange={(event) => {
                    setSearchTerm(event.target.value);
                  }}
                />
              </div>


              <select
                value={categoryFilter}
                onChange={(event) => {
                  setCategoryFilter(event.target.value);
                }}
                aria-label="服務分類"
              >
                <option value="all">
                  所有分類
                </option>

                {CATEGORY_OPTIONS.map((option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.description}
                  </option>
                ))}
              </select>


              <select
                value={statusFilter}
                onChange={(event) => {
                  setStatusFilter(event.target.value);
                }}
                aria-label="服務狀態"
              >
                <option value="all">所有狀態</option>
                <option value="active">啟用中</option>
                <option value="inactive">已停用</option>
              </select>

            </div>


            {/* Table */}
            <div className="table-wrapper">

              <table className="service-table">

                <thead>
                  <tr>
                    <th>服務資訊</th>
                    <th>服務分類</th>
                    <th>狀態</th>
                    <th>最後更新</th>
                    <th>操作</th>
                  </tr>
                </thead>


                <tbody>

                  {isLoading ? (

                    <tr>
                      <td colSpan={5} className="empty-state">
                        正在載入企業服務...
                      </td>
                    </tr>

                  ) : filteredServices.length === 0 ? (

                    <tr>
                      <td colSpan={5} className="empty-state">
                        目前沒有符合條件的企業服務
                      </td>
                    </tr>

                  ) : (

                    filteredServices.map((service) => (

                      <tr key={service.id}>

                        <td>
                          <div className="service-info">
                            <strong>
                              {service.name}
                            </strong>

                            <span>
                              {service.code}
                            </span>
                          </div>
                        </td>


                        <td>
                          <span className="category-label">
                            {getCategoryLabel(service.category)}
                          </span>
                        </td>


                        <td>
                          <span
                            className={
                              service.is_active
                                ? "status-badge active"
                                : "status-badge inactive"
                            }
                          >
                            {service.is_active
                              ? "啟用中"
                              : "已停用"}
                          </span>
                        </td>


                        <td>
                          {formatDate(service.updated_at)}
                        </td>


                        <td>
                          <div className="table-actions">

                            <button
                              type="button"
                              onClick={() => {
                                openEditModal(service);
                              }}
                            >
                              編輯
                            </button>

                            <button
                              type="button"
                              onClick={() => {
                                handleToggleStatus(service);
                              }}
                            >
                              {service.is_active
                                ? "停用"
                                : "啟用"}
                            </button>

                            <button
                              type="button"
                              className="delete-action"
                              onClick={() => {
                                handleDelete(service);
                              }}
                            >
                              刪除
                            </button>

                          </div>
                        </td>

                      </tr>

                    ))

                  )}

                </tbody>

              </table>

            </div>

          </section>

        </section>

      </main>


      {/* Create / Edit Modal */}
      {isModalOpen && (

        <div
          className="modal-overlay"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeModal();
            }
          }}
        >

          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
          >

            <div className="modal-header">

              <div>
                <h3 id="modal-title">
                  {editingService
                    ? "編輯企業服務"
                    : "新增企業服務"}
                </h3>

                <p>
                  請填寫企業服務的基本資訊。
                </p>
              </div>

              <button
                type="button"
                className="modal-close"
                onClick={closeModal}
                aria-label="關閉"
              >
                ×
              </button>

            </div>


            <form onSubmit={handleSubmit}>

              <div className="form-group">

                <label htmlFor="code">
                  服務代碼
                </label>

                <input
                  id="code"
                  name="code"
                  type="text"
                  placeholder="例如 CONNECT-001"
                  value={formData.code}
                  onChange={handleInputChange}
                  required
                  minLength={3}
                  maxLength={30}
                  pattern="[A-Z0-9]+(-[A-Z0-9]+)*"
                />

              </div>


              <div className="form-group">

                <label htmlFor="name">
                  服務名稱
                </label>

                <input
                  id="name"
                  name="name"
                  type="text"
                  placeholder="請輸入服務名稱"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  maxLength={150}
                />

              </div>


              <div className="form-group">

                <label htmlFor="category">
                  服務分類
                </label>

                <select
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  required
                >

                  {CATEGORY_OPTIONS.map((option) => (
                    <option
                      key={option.value}
                      value={option.value}
                    >
                      {option.description}
                    </option>
                  ))}

                </select>

              </div>


              <div className="form-group">

                <label htmlFor="description">
                  服務說明
                </label>

                <textarea
                  id="description"
                  name="description"
                  placeholder="請描述企業服務的內容與用途"
                  value={formData.description}
                  onChange={handleInputChange}
                  required
                  maxLength={2000}
                  rows={4}
                />

              </div>


              <label className="checkbox-group">

                <input
                  type="checkbox"
                  name="is_active"
                  checked={formData.is_active}
                  onChange={handleInputChange}
                />

                <span>
                  啟用此服務
                </span>

              </label>


              {error && (
                <div className="error-message" role="alert">
                  {error}
                </div>
              )}


              <div className="modal-actions">

                <button
                  type="button"
                  className="secondary-button"
                  onClick={closeModal}
                  disabled={isSubmitting}
                >
                  取消
                </button>

                <button
                  type="submit"
                  className="primary-button"
                  disabled={isSubmitting}
                >
                  {isSubmitting
                    ? "儲存中..."
                    : editingService
                      ? "儲存修改"
                      : "建立服務"}
                </button>

              </div>

            </form>

          </section>

        </div>

      )}

    </div>
  );
}

export default App;
