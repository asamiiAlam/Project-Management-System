import { useState } from "react";
import "./CreateProject.css";

function CreateProject({ onSaveProject, onUpdateProject, editingProject }) {
  const [name, setName] = useState(editingProject?.name ?? "");
  const [role, setRole] = useState(editingProject?.role ?? "");
  const [projectName, setprojectName] = useState(
    editingProject?.projectName ?? "",
  );
  const [description, setDescription] = useState(
    editingProject?.description ?? "",
  );

  const handleSave = () => {
    if (!name.trim() || !role || !projectName.trim()) {
      alert("Please fill in all fields");
      return;
    }

    const newProject = {
      id: crypto.randomUUID(), //js built-in api
      name: name.trim(),
      role: role,
      projectName: projectName.trim(),
      description: description.trim(),
    };

    if (editingProject) {
      const updatedProject = {
        ...newProject,
        id: editingProject.id,
      };
      onUpdateProject(updatedProject);
    } else {
      onSaveProject(newProject);
    }
  };

  return (
    <div className="create-project-form">
      <h2>Create Project</h2>
      <p>Fill up the form to create a Project</p>

      <label htmlFor="name">Name</label>
      <input
        type="text"
        id="name"
        placeholder="Enter your name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      ></input>

      <label htmlFor="role">Role</label>
      <select id="role" value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="" disabled>
          Select your Role
        </option>

        <option value="Frontend">Frontend</option>
        <option value="Backend">Backend</option>
        <option value="SQA">SQA</option>
        <option value="UI/UX">UI/UX</option>
        <option value="DevOps">DevOps</option>
      </select>

      <label htmlFor="projectName">Project Name</label>
      <input
        type="text"
        id="projectName"
        placeholder="Enter your Project name"
        value={projectName}
        onChange={(e) => setprojectName(e.target.value)}
      ></input>

      <label htmlFor="description">Description</label>
      <textarea
        id="description"
        placeholder="Description about the project"
        rows={4}
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <button type="button" onClick={handleSave}>
        Save Project
      </button>
    </div>
  );
}
export default CreateProject;
