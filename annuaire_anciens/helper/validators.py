# coding=utf-8
"""
Validators custom pour WTForms
"""
from wtforms import ValidationError
from datetime import datetime

class RequiredIfOther(object):
    """
    Forcer le field à être non-null si "other-field" est non null (field SI ET SEULEMENT SI other_field)

    :param other_field_name: str, required, le nom de l'autre field
    :param message: Message d'erreur à mettre dans la ValidationError
    @raise: ValidationError si other_field_name n'est pas dans le formulaire
    @raise: ValidationError if (field XOR other_field)
    """
    def __init__(self, other_field_name, message=None):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.other_field_name]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.other_field_name)
        if not self.__contains_data(field) and self.__contains_data(other):
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.other_field_name,
                'other_name': self.other_field_name
            }
            if self.message is None:
                self.message = field.gettext('You must set a value if %(other_name)s is not null.')

            raise ValidationError(self.message % d)


    def __contains_data(self, field):
        return field.data is not None and (field.data!='')

class ValidDateMonth(object):
    """
    Valide les dates au format : mm/yyyy (%m/%Y)

    :param message: Message d'erreur à retourner si ValidationError
    @raise: ValidationError si la date est mal formattée
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        try:
            datetime.strptime(field.data,'%m/%Y')
        except ValueError:
            if self.message is None:
                self.message = field.gettext("Date must formatted mm/yyyy")

            raise ValidationError(self.message)