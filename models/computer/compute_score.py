from odoo import fields, models

class Computer(models.AbstractModel):
    _inherit = "assets_computer"

    cpu_score = fields.Float()
    gpu_score = fields.Float()

    performance_score = fields.Float()

    def action_compute_score(self):
        score = self.env["assets_component_score"]

        main_score = 0.0

        gpu_max = 17000.0
        cpu_max = 10000.0

        for record in self:
            cpu_score = 0.0
            gpu_score = 0.0

            if record.cpu:
                cpu = score.search(
                    [   ('component_type','=','cpu'),
                        ('name','=',record.cpu)],
                    limit = 1
                )
                cpu_score = cpu.score if cpu else 0
            else : cpu_score = 0

            if record.gpu:
                gpu = score.search(
                    [   ('component_type','=','gpu'),
                        ('name','=', record.gpu)],
                    limit = 1
                )
                gpu_score = gpu.score if gpu else 0
            else: gpu_score = 0

        gpu = self.normalize(gpu_score, gpu_max)
        cpu = self.normalize(cpu_score, cpu_max)

        main_score = (0.6*gpu)+(0.4*cpu)

        record.cpu_score = cpu
        record.gpu_score = gpu
        record.performance_score = main_score


    
    def normalize(self, number, max_val):
        return (number /max_val) *100

            