if (DISTRIBUTED)
    set(QuEST_SRC_CPU_ARCHITECTURE_DEPENDENT
        ${CMAKE_CURRENT_SOURCE_DIR}/QuEST_cpu_distributed.c
    )
else()
    set(QuEST_SRC_CPU_ARCHITECTURE_DEPENDENT
        ${CMAKE_CURRENT_SOURCE_DIR}/QuEST_cpu_local.c
    )
endif()

set(QuEST_SRC_ARCHITECTURE_DEPENDENT
    ${CMAKE_CURRENT_SOURCE_DIR}/QuEST_cpu.c
    ${QuEST_SRC_CPU_ARCHITECTURE_DEPENDENT}
    PARENT_SCOPE
) 


