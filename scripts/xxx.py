# BEGIN (write your solution here)
def validate(course):
    errors = {}
    if not course['paid']:
        errors['paid'] = "Can't be blank"
    if not course['title']:
        errors['title'] = "Can't be blank"
    return errors
# END
#
# <!doctype html>
# <html>
#   <head>
#     <title>Example application</title>
#   </head>
#   <body>
# <!-- BEGIN (write your solution here) -->
# <form action="/courses", method="post">
# <div>
#   <label>
#     Title
#     <input type="text", name="title" value=courses>
#   </label>
# </div>
# <div>
# <label>
# Paid
# </label>
# <select>
#   <option disabled selected value> -- select an option -- </option>
#   <option "value"=True>Yes</option>
#   <option "value"=False>No</option>
# </select>
# </div>
# <input type="submit" value="Create">
# </form>
# <!-- END -->
#   </body>
# </html>

# BEGIN (write your solution here)
# from validator import validate
# END

# # BEGIN (write your solution here)
# @app.post('/courses')
# def post_courses():
#     new_course = request.form.to_dict()
#     errors = validate(new_course)
#     if errors:
#         return render_template(
#         'courses/new.html'
#         # errors=errors
#         )
#     repo.save(new_course)
#     return redirect('/courses', code=302)
#
#
# @app.route('/courses/new')
# def new_courses():
#     course = {
#         'title' = ''
#         'paid' = ''
#     }
#     return render_template(
#         'courses/new.html'
#         # errors=errors
#     )
# # END