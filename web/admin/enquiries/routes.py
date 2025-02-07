from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web.admin.enquiries.models import Enquiry

bp = Blueprint('enquiries', __name__, url_prefix='/admin/enquiries')

@bp.route('/', methods=('GET',))
def index():
    enquiries = Enquiry.query.all()
    return render_template('admin/enquiries/index.html', enquiries=enquiries, title='Enquiries')


@bp.route('view/<int:pk>', methods=('GET',))
def view(pk):
    enquiry = Enquiry.query.filter_by(id=pk).first()
    return render_template('admin/enquiries/view.html', enquiry=enquiry, title=enquiry.title)

