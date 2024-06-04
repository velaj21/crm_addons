from odoo import models, api


class MyCronJob(models.AbstractModel):
    _name = 'my.cron.job'

    @api.model
    def run_cron_job(self):
        print("Hello, Odoo!")
