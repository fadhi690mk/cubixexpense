from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ==========================================
    # AUTHENTICATION URLS
    # ==========================================
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # ==========================================
    # DASHBOARD
    # ==========================================
    path('', views.dashboard, name='dashboard'),
    
    # ==========================================
    # FUND URLS
    # ==========================================
    path('funds/', views.FundListView.as_view(), name='fund-list'),
    path('funds/create/', views.FundCreateView.as_view(), name='fund-create'),
    path('funds/<int:pk>/', views.FundDetailView.as_view(), name='fund-detail'),
    path('funds/<int:pk>/edit/', views.FundUpdateView.as_view(), name='fund-update'),
    path('funds/<int:pk>/delete/', views.FundDeleteView.as_view(), name='fund-delete'),
    
    # ==========================================
    # EXPENSE URLS
    # ==========================================
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expenses/<int:pk>/add-documents/', views.add_expense_documents, name='add-expense-documents'),
    path('documents/<int:pk>/delete/', views.ExpenseDocumentDeleteView.as_view(), name='document-delete'),
    path('documents/<int:pk>/download/', views.download_expense_document, name='document-download'),
    path('documents/<int:pk>/view/', views.view_expense_document, name='document-view'),
    
    # ==========================================
    # CONTRIBUTOR URLS
    # ==========================================
    path('contributors/', views.ContributorListView.as_view(), name='contributor-list'),
    path('contributors/create/', views.ContributorCreateView.as_view(), name='contributor-create'),
    path('contributors/<int:pk>/edit/', views.ContributorUpdateView.as_view(), name='contributor-update'),
    path('contributors/<int:pk>/delete/', views.ContributorDeleteView.as_view(), name='contributor-delete'),
    
    # ==========================================
    # CATEGORY URLS
    # ==========================================
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # ==========================================
    # REPORT URLS
    # ==========================================
    path('reports/', views.ReportDashboardView.as_view(), name='report-dashboard'),
    path('reports/export/', views.report_export, name='report-export'),
    
    # ==========================================
    # ACTIVITY LOG URLS
    # ==========================================
    path('activity-logs/', views.ActivityLogListView.as_view(), name='activity-logs'),
    
    # ==========================================
    # TODO URLS (PLANNED EXPENSES)
    # ==========================================
    path('todos/', views.TodoListView.as_view(), name='todo-list'),
    path('todos/create/', views.TodoCreateView.as_view(), name='todo-create'),
    path('todos/<int:pk>/edit/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('todos/<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('todos/<int:pk>/convert/', views.TodoConvertView.as_view(), name='todo-convert'),
    
    # ==========================================
    # DELETED RECORDS URLS (SUPERADMIN ONLY)
    # ==========================================
    path('deleted-records/', views.DeletedRecordsListView.as_view(), name='deleted-records'),
    path('deleted-records/funds/', views.DeletedFundsView.as_view(), name='deleted-funds'),
    path('deleted-records/expenses/', views.DeletedExpensesView.as_view(), name='deleted-expenses'),
    path('deleted-records/categories/', views.DeletedCategoriesView.as_view(), name='deleted-categories'),
    path('deleted-records/restore/', views.RestoreRecordView.as_view(), name='restore-record'),
]