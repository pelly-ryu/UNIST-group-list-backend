from app import db

from flask_restplus import Resource, Namespace, fields

from app import db
from app.base.decorators import login_required
from app.notice.models import Notice


ns = Namespace('Notice', description='Notice Board')

notice_fields = ns.model('notice_fields', {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'is_shown': fields.Boolean,
    'is_public': fields.Boolean
})

class NoticeDetail(Resource):
    def get(self, notice_id):
        notice = Notice.query.filter_by(id=notice_id)
        if not notice or notice.count() == 0:
            ns.abort(404, message="Notice {} doesn't exist".format(notice_id))
        serialized_list = list(map(lambda x: x.serialize(), notice))
        return serialized_list


class NoticeRegister(Resource):
    parser = ns.parser()
    parser.add_argument("title", type=str, location='form')
    parser.add_argument("contents", location='form')
    parser.add_argument("is_shown", type=bool, location='form')
    parser.add_argument("is_public", type=bool, location='form')

    @ns.marshal_with(notice_fields)
    @ns.doc(parser=parser)
    @login_required
    def post(self):
        args = self.parser.parse_args()
        title = args.get('title')
        contents = args.get('contents')
        is_shown = args.get('is_shown')
        is_public = args.get('is_public')

        if title and contents and is_shown and is_public:
            notice = Notice(title=title,
                            contents=contents,
                            is_shown=is_shown,
                            is_public=is_public)
            db.session.add(notice)
            db.session.commit()
            return notice
        else:
            ns.abort(400, message='Not enough fields for register.')


class NoticeList(Resource):
    parser = ns.parser()
    parser.add_argument('page', type=int)
    parser.add_argument('size', type=int)
    
    @ns.doc(parser=parser)
    def get(self):
        args = self.parser.parse_args()
        page = args.get("page") or 1
        size = args.get("size") or 3

        notice_list = Notice.query.filter_by(is_shown=True).paginate(page=page, per_page=size).items
        if not notice_list:
            ns.abort(404, message="Notice {} page doesn't exist".format(page))
        serialized_list = list(map(lambda x: x.serialize(), notice_list))
        return serialized_list


ns.add_resource(NoticeDetail, '/<notice_id>')
ns.add_resource(NoticeList, '/list')
ns.add_resource(NoticeRegister, '')
