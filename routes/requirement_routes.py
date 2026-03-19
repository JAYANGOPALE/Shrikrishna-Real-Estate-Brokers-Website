from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from forms.requirement_forms import RequirementForm
from services.requirement_service import (
    create_requirement, 
    get_user_requirements, 
    get_requirement_by_id, 
    update_requirement, 
    delete_requirement,
    get_all_requirements,
    update_requirement_status
)

requirement_bp = Blueprint('requirement', __name__)

# --- USER ROUTES ---

@requirement_bp.route('/post', methods=['GET', 'POST'])
@login_required
def post_requirement():
    """Route for users to post a new requirement."""
    if current_user.is_admin:
        flash("Admins can't post requirements.", "warning")
        return redirect(url_for('admin.dashboard'))

    form = RequirementForm()
    if form.validate_on_submit():
        data = {
            'requirement_type': form.requirement_type.data,
            'property_type': form.property_type.data,
            'location': form.location.data,
            'budget_min': form.budget_min.data,
            'budget_max': form.budget_max.data,
            'bhk': form.bhk.data,
            'description': form.description.data,
            'contact_preference': form.contact_preference.data
        }
        create_requirement(current_user.id, data)
        flash('Property requirement posted successfully!', 'success')
        return redirect(url_for('requirement.my_requirements'))
    
    return render_template('post_requirement.html', form=form, title="Post Requirement")

@requirement_bp.route('/my-requirements')
@login_required
def my_requirements():
    """Route for users to view their requirements."""
    if current_user.is_admin:
        return redirect(url_for('requirement.admin_requirements'))
        
    requirements = get_user_requirements(current_user.id)
    return render_template('my_requirements.html', requirements=requirements)

@requirement_bp.route('/edit/<int:req_id>', methods=['GET', 'POST'])
@login_required
def edit_requirement(req_id):
    """Route for users to edit their requirement."""
    req = get_requirement_by_id(req_id)
    
    if not req or (req.user_id != current_user.id and not current_user.is_admin):
        flash('Unauthorized access or requirement not found.', 'danger')
        return redirect(url_for('requirement.my_requirements'))
    
    form = RequirementForm(obj=req)
    if form.validate_on_submit():
        data = {
            'requirement_type': form.requirement_type.data,
            'property_type': form.property_type.data,
            'location': form.location.data,
            'budget_min': form.budget_min.data,
            'budget_max': form.budget_max.data,
            'bhk': form.bhk.data,
            'description': form.description.data,
            'contact_preference': form.contact_preference.data
        }
        update_requirement(req_id, data)
        flash('Requirement updated successfully!', 'success')
        return redirect(url_for('requirement.my_requirements'))
    
    return render_template('post_requirement.html', form=form, title="Edit Requirement", is_edit=True)

@requirement_bp.route('/delete/<int:req_id>', methods=['POST'])
@login_required
def delete_req(req_id):
    """Route for users to delete their requirement."""
    req = get_requirement_by_id(req_id)
    
    if not req or (req.user_id != current_user.id and not current_user.is_admin):
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('requirement.my_requirements'))
    
    delete_requirement(req_id)
    flash('Requirement deleted successfully.', 'success')
    return redirect(url_for('requirement.my_requirements'))

# --- ADMIN ROUTES ---

@requirement_bp.route('/admin/all')
@login_required
def admin_requirements():
    """Route for admin to view all requirements with filtering."""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    filters = {
        'location': request.args.get('location'),
        'property_type': request.args.get('property_type'),
        'status': request.args.get('status'),
        'budget_min': request.args.get('budget_min', type=float),
        'budget_max': request.args.get('budget_max', type=float)
    }
    
    requirements = get_all_requirements(filters)
    return render_template('admin/admin_requirements.html', requirements=requirements, filters=filters)

@requirement_bp.route('/admin/update-status/<int:req_id>', methods=['POST'])
@login_required
def update_status(req_id):
    """Route for admin to update status of a requirement."""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Contacted', 'Closed']:
        update_requirement_status(req_id, new_status)
        flash(f'Status updated to {new_status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
        
    return redirect(url_for('requirement.admin_requirements'))
