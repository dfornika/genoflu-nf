process GENOFLU {
    tag "$meta.id"
    label 'process_low'

    // TODO nf-core: See section in main README for further information regarding finding and adding container addresses to the section below.
    conda "${moduleDir}/environment.yml"
    container "${ workflow.containerEngine in ['singularity', 'apptainer'] && !task.ext.singularity_pull_docker_container ?
        'community.wave.seqera.io/library/genoflu:1.07--6743e401a4494e3a':
        'quay.io/biocontainers/genoflu:1.07--hdfd78af_0' }"

    input:
    tuple val(meta), path(fasta)

    output:
    // TODO nf-core: Named file extensions MUST be emitted for ALL output channels
    tuple val(meta), path("*_genoflu_stats.tsv"), emit: stats_tsv
    tuple val(meta), path("*_genoflu_stats.json"), emit: stats_json
    tuple val("${task.process}"), val('genoflu'), eval("genoflu.py --version | cut -d ' ' -f 3"), topic: versions, emit: versions_genoflu

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    """
    genoflu.py \\
        $args \\
        -f $fasta
    mv ${prefix}*_stats.tsv ${prefix}_genoflu_stats.tsv

    parse_genoflu_stats.py -i ${prefix}_genoflu_stats.tsv > ${prefix}_genoflu_stats.json
    """

    stub:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    // TODO nf-core: A stub section should mimic the execution of the original module as best as possible
    //               Have a look at the following examples:
    //               Simple example: https://github.com/nf-core/modules/blob/624977dfaf562211e68a8a868ca80acc8461f1ac/modules/nf-core/cutadapt/main.nf#L34-L46
    //               Complex example: https://github.com/nf-core/modules/blob/88d43dad73a675e66bff49ebb57fe657a5909018/modules/nf-core/bedtools/split/main.nf#L32-L43
    // TODO nf-core: If the module doesn't use arguments ($args), you SHOULD remove:
    //               - The definition of args `def args = task.ext.args ?: ''` above.
    //               - The use of the variable in the script `echo $args ` below.
    """
    echo $args
    
    touch ${prefix}_genoflu_stats.tsv
    """
}
