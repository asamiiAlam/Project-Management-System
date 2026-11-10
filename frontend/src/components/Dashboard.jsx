import "./Dashboard.css";
import { useState } from "react";
import CreateProject from "./CreateProject";

function Dashboard({ onLogout }) {
  const [activePage, setActivePage] = useState("dashboard");
  const [projects, setProjects] = useState([]);
  const [editingProject, setEditingProject] = useState(null);

  const handleAddProject = (newProject) => {
    setProjects((previousProjects) => [...previousProjects, newProject]);
    setActivePage("dashboard");
  };

  const handleEditProject = (project) => {
    setEditingProject(project);
    setActivePage("create-project");
  };

  const handleCreateProject = () => {
    setEditingProject(null);
    setActivePage("create-project");
  };

  const handleUpdateProject = (updatedProject) => {
    setProjects((previousProjects) =>
      previousProjects.map((project) => {
        if (project.id === updatedProject.id) {
          return updatedProject;
        }
        return project;
      }),
    );

    setActivePage("dashboard");
    setEditingProject(null);
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <h2>Admin Panel</h2>

        <nav>
          <p onClick={() => setActivePage("dashboard")}>Dashboard</p>
          <p>Users</p>

          <p onClick={handleCreateProject}>Create Project</p>

          <p>settings</p>

          <button type="button" onClick={onLogout}>
            Logout
          </button>
        </nav>
      </aside>

      <main>
        <header className="navbar">
          <h2>Dashboard</h2>

          <div className="navbar-right">
            <span>🔔</span>
            <span>👤 Admin</span>
          </div>
        </header>

        <section className="dashboard-content">
          {activePage === "dashboard" ? (
            <div>
              <h1>Welcome to your Dashboard!</h1>
              <p>Here is your dashboard overview</p>

              <button type="button" onClick={handleCreateProject}>
                + Create Project
              </button>

              <div className="summary-cards">
                {projects.length === 0 ? (
                  <p>
                    No projects yet. Click "Create Project" to add your first
                    project.
                  </p>
                ) : (
                  projects.map((project, index) => (
                    <div className="summary-card" key={index}>
                      <h3>Name: {project.name}</h3>
                      <p>Role: {project.role}</p>
                      <p>Project: {project.projectName}</p>
                      <p>
                        Description:
                        {project.description || "No description added"}
                      </p>
                      <button
                        type="button"
                        onClick={() => handleEditProject(project)}
                      >
                        Edit
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <CreateProject
              onSaveProject={handleAddProject}
              editingProject={editingProject}
              onUpdateProject={handleUpdateProject}
            />
          )}
        </section>
      </main>
    </div>
  );
}
export default Dashboard;
