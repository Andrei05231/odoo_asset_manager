import re
from odoo import fields, models
from odoo.exceptions import ValidationError

class Computer(models.AbstractModel):
    _inherit = "assets_computer"

    cpu_score = fields.Float()
    gpu_score = fields.Float()

    performance_score = fields.Float()

    def action_compute_score(self):
        score = self.env["assets_component_score"]

        main_score = 0.0

        gpu_max = 17000.0
        cpu_max = 1000.0

        for record in self:
            cpu_score = 0.0
            gpu_score = 0.0

            if not record.cpu or not record.gpu:
                raise ValidationError("CPU and GPU required to calculate score.")
            
            # computer might have multiple gpus separated by ','
            if ','in record.gpu:
                processed_gpu = self.get_descrete_gpu(record.gpu)
            else:
                processed_gpu = record.gpu

            processed_cpu = self.process_cpu_name(record.cpu)

            cpu = score.search(
                [   ('component_type','=','cpu'),
                    ('name','=',processed_cpu)],
                limit = 1
            )
            gpu = score.search(
                [   ('component_type','=','gpu'),
                    ('name','=', processed_gpu)],
                limit = 1
            )

            if not cpu: 
                raise ValidationError(f'No score found for CPU: %s'%processed_cpu)            
            if not gpu:
                raise ValidationError(f'No score found for GPU: %s'%processed_gpu)
            
            cpu_score = cpu.score if cpu.score <1000.0 else 1000.0
            gpu_score = gpu.score

            gpu = self.normalize_score(gpu_score, gpu_max)
            cpu = self.normalize_score(cpu_score, cpu_max)

            main_score = (0.6*gpu)+(0.4*cpu)

            record.cpu_score = cpu
            record.gpu_score = gpu
            record.performance_score = main_score


    
    def normalize_score(self, number, max_val):
        return (number /max_val) *100
    
    def get_descrete_gpu(self, gpu_list):
        descrete_markers = (
        'nvidia',
        'geforce',
        'rtx',
        'gtx',
        'quadro',
        'radeon',
        'rx ',
        'arc',
    )
        gpus = self.split_gpu_names(gpu_list)
        
        for gpu in gpus:
            if any(marker in gpu.lower() for marker in descrete_markers):
                return gpu
            
        return gpus[0]


    def split_gpu_names(self, gpu_field):
        return [part.strip() for part in re.split(r'[;,]', gpu_field) if part.strip()]

    def process_cpu_name(self, cpu_name):
        # Remove generation info at the start (e.g., "11th Gen")
        cpu_name = re.sub(r'^\d+\w+\s+Gen\s+', '', cpu_name)
        # Remove (R), (TM)
        cpu_name = re.sub(r'\(R\)|\(TM\)', '', cpu_name)
        # Remove anything after @ (frequency info) or in brackets
        cpu_name = re.sub(r'\[.*\]', '', cpu_name)
        # Remove extra spaces
        cpu_name = ' '.join(cpu_name.split())
        return cpu_name
